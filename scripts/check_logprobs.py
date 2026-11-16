"""Teste réellement l'accès aux logprobs (prompt et complétion) de chaque voie d'API (todo P1).

Un appel minimal par voie : un court extrait de code en entrée, 1 à 16 tokens en sortie.
Coût total estimé : moins de 0,01 $. Les clés sont lues dans .env et ne sont jamais affichées
ni écrites : les réponses brutes sauvegardées sont nettoyées de toute valeur de clé.

Usage :
    uv run python scripts/check_logprobs.py --dry-run          # liste les appels, n'envoie rien
    uv run python scripts/check_logprobs.py                    # toutes les voies dont la clé existe
    uv run python scripts/check_logprobs.py --only openrouter,together

Sorties : tableau dans le terminal + results/<date>_check-logprobs/ (config.json, summary.json,
raw/<voie>.json). Reporter ensuite les résultats dans docs/model_access.md.
"""

import argparse
import datetime as dt
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

import truststore

truststore.inject_into_ssl()

ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = ROOT / ".env"
TIMEOUT = 90

# Extrait de code testé : court, banal, identique pour toutes les voies.
CODE = 'def add(a, b):\n    """Return the sum of a and b."""\n    return a + b\n'

OPENROUTER_MODELS = [
    "openai/gpt-5",
    "google/gemini-2.5-flash",
    "mistralai/mistral-small-24b-instruct-2501",
    "mistralai/mistral-small-3.1-24b-instruct",
    "mistralai/mistral-small-3.2-24b-instruct",
    "deepseek/deepseek-chat",
    "deepseek/deepseek-chat-v3-0324",
    "meta-llama/llama-3.3-70b-instruct",
]


# --------------------------------------------------------------------------- fonctions pures


def parse_env(text: str) -> dict[str, str]:
    """Lit un fichier .env simple (CLE=valeur), ignore commentaires et valeurs vides."""
    env = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        value = value.strip().strip('"').strip("'")
        if value:
            env[key.strip()] = value
    return env


def scrub(text: str, secrets: list[str]) -> str:
    """Remplace toute valeur de clé par *** (au cas où une erreur la renverrait)."""
    for s in secrets:
        if s:
            text = text.replace(s, "***")
    return text


def count_chat_logprobs(resp: dict) -> int:
    """Tokens de complétion avec logprob, format OpenAI chat (choices[0].logprobs.content)."""
    try:
        content = resp["choices"][0]["logprobs"]["content"]
    except (KeyError, IndexError, TypeError):
        return 0
    return len(content or [])


def count_together_prompt_logprobs(resp: dict) -> int:
    """Tokens du prompt avec logprob, format Together completions avec echo."""
    n = 0
    for part in resp.get("prompt") or []:
        lp = (part or {}).get("logprobs") or {}
        n += sum(1 for x in lp.get("token_logprobs") or [] if x is not None)
    return n


def count_together_completion_logprobs(resp: dict) -> int:
    try:
        lp = resp["choices"][0]["logprobs"] or {}
    except (KeyError, IndexError, TypeError):
        return 0
    return sum(1 for x in lp.get("token_logprobs") or [] if x is not None)


def find_prompt_logprobs(obj, path: str = "") -> list[str]:
    """Chemins des champs dont le nom contient 'prompt_logprob' et qui sont non vides.

    Sert pour l'API Mistral, dont la forme de réponse à `prompt_logprobs` n'est pas documentée.
    """
    found = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{path}.{k}" if path else k
            if "prompt_logprob" in k.lower() and v:
                found.append(p)
            found += find_prompt_logprobs(v, p)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            found += find_prompt_logprobs(v, f"{path}[{i}]")
    return found


def count_gemini_logprobs(resp: dict) -> int:
    try:
        return len(resp["candidates"][0]["logprobsResult"]["chosenCandidates"] or [])
    except (KeyError, IndexError, TypeError):
        return 0


# --------------------------------------------------------------------------- appels


def post(url: str, payload: dict, headers: dict) -> tuple[int, dict | str]:
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", **headers},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="replace")
        try:
            return e.code, json.loads(body)
        except json.JSONDecodeError:
            return e.code, body
    except (urllib.error.URLError, TimeoutError) as e:
        return 0, f"erreur réseau : {e}"


def chat_messages() -> list[dict]:
    return [{"role": "user", "content": CODE}]


def build_calls(env: dict) -> list[dict]:
    """Liste des appels : nom, clé requise, url, payload, en-têtes, fonction d'analyse."""
    calls = []

    def chat_result(resp):
        return {"completion_lp": count_chat_logprobs(resp), "prompt_lp": None}

    for m in OPENROUTER_MODELS:
        payload = {
            "model": m,
            "messages": chat_messages(),
            "max_tokens": 16,
            "logprobs": True,
            "top_logprobs": 1,
            # sans ce champ, OpenRouter ignorerait silencieusement logprobs
            "provider": {"require_parameters": True},
            "usage": {"include": True},
        }
        if m.startswith("openai/gpt-5"):
            payload["reasoning"] = {"effort": "minimal"}
        calls.append(
            dict(
                name=f"openrouter:{m}",
                key="OPENROUTER_API_KEY",
                url="https://openrouter.ai/api/v1/chat/completions",
                payload=payload,
                auth="bearer",
                parse=chat_result,
            )
        )

    calls.append(
        dict(
            name="together:llama-3.3-70b (echo)",
            key="TOGETHER_API_KEY",
            url="https://api.together.xyz/v1/completions",
            payload={
                "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
                "prompt": CODE,
                "max_tokens": 1,
                "logprobs": 1,
                "echo": True,
            },
            auth="bearer",
            parse=lambda r: {
                "completion_lp": count_together_completion_logprobs(r),
                "prompt_lp": count_together_prompt_logprobs(r),
            },
        )
    )
    calls.append(
        dict(
            name="mistral:mistral-small-latest (prompt_logprobs)",
            key="MISTRAL_API_KEY",
            url="https://api.mistral.ai/v1/chat/completions",
            payload={
                "model": "mistral-small-latest",
                "messages": chat_messages(),
                "max_tokens": 1,
                "logprobs": True,
                "prompt_logprobs": True,
            },
            auth="bearer",
            parse=lambda r: {
                "completion_lp": count_chat_logprobs(r),
                "prompt_lp": len(find_prompt_logprobs(r)) or 0,
                "prompt_lp_fields": find_prompt_logprobs(r),
            },
        )
    )
    calls.append(
        dict(
            name="gemini:gemini-2.5-flash (AI Studio)",
            key="GEMINI_API_KEY",
            url="https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent",
            payload={
                "contents": [{"role": "user", "parts": [{"text": CODE}]}],
                "generationConfig": {
                    "maxOutputTokens": 5,
                    "responseLogprobs": True,
                    "logprobs": 1,
                    "thinkingConfig": {"thinkingBudget": 0},
                },
            },
            auth="goog",
            parse=lambda r: {"completion_lp": count_gemini_logprobs(r), "prompt_lp": None},
        )
    )
    calls.append(
        dict(
            name="openai:gpt-5",
            key="OPENAI_API_KEY",
            url="https://api.openai.com/v1/chat/completions",
            payload={
                "model": "gpt-5",
                "messages": chat_messages(),
                "max_completion_tokens": 16,
                "reasoning_effort": "minimal",
                "logprobs": True,
                "top_logprobs": 1,
            },
            auth="bearer",
            parse=chat_result,
        )
    )
    calls.append(
        dict(
            name="deepseek:deepseek-chat",
            key="DEEPSEEK_API_KEY",
            url="https://api.deepseek.com/chat/completions",
            payload={
                "model": "deepseek-chat",
                "messages": chat_messages(),
                "max_tokens": 5,
                "logprobs": True,
                "top_logprobs": 1,
            },
            auth="bearer",
            parse=chat_result,
        )
    )
    return calls


def headers_for(call: dict, env: dict) -> dict:
    key = env[call["key"]]
    if call["auth"] == "goog":
        return {"x-goog-api-key": key}
    return {"Authorization": f"Bearer {key}"}


def error_message(body) -> str:
    if isinstance(body, dict):
        err = body.get("error", body)
        if isinstance(err, dict):
            return str(err.get("message", err))[:160]
        return str(err)[:160]
    return str(body)[:160]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dry-run", action="store_true", help="liste les appels sans rien envoyer")
    ap.add_argument("--only", default="", help="voies à tester, ex. openrouter,together")
    args = ap.parse_args()

    env = parse_env(ENV_FILE.read_text(encoding="utf-8")) if ENV_FILE.exists() else {}
    calls = build_calls(env)
    if args.only:
        wanted = {w.strip() for w in args.only.split(",")}
        calls = [c for c in calls if c["name"].split(":")[0] in wanted]

    runnable = [c for c in calls if c["key"] in env]
    skipped = [c for c in calls if c["key"] not in env]
    print(f".env : {'trouvé' if ENV_FILE.exists() else 'ABSENT'} ; clés présentes : "
          f"{', '.join(sorted(k for k in env if k.endswith('_API_KEY'))) or 'aucune'}")
    print(f"{len(runnable)} appel(s) à faire, {len(skipped)} sauté(s) faute de clé.")
    print("Coût estimé : < 0,001 $ par appel (~40 tokens in, <= 16 out), < 0,01 $ au total.\n")
    for c in skipped:
        print(f"  [sauté]  {c['name']} (pas de {c['key']})")
    if args.dry_run:
        for c in runnable:
            print(f"  [prévu]  {c['name']}")
        return 0
    if not runnable:
        print("Rien à tester : remplir .env (voir docs/model_access.md).")
        return 1

    today = dt.date.today().isoformat()
    out = ROOT / "results" / f"{today}_check-logprobs"
    (out / "raw").mkdir(parents=True, exist_ok=True)
    secrets = list(env.values())
    config = {
        "date": today,
        "script": "scripts/check_logprobs.py",
        "code_snippet": CODE,
        "calls": [{"name": c["name"], "url": c["url"], "payload": c["payload"]} for c in runnable],
    }
    (out / "config.json").write_text(json.dumps(config, indent=2, ensure_ascii=False), "utf-8")

    summary = []
    print(f"{'voie':55} {'HTTP':>4} {'lp sortie':>9} {'lp prompt':>9}  remarque")
    for c in runnable:
        status, body = post(c["url"], c["payload"], headers_for(c, env))
        safe = scrub(json.dumps(body, indent=2, ensure_ascii=False), secrets)
        fname = c["name"].replace(":", "__").replace("/", "_").replace(" ", "_")
        (out / "raw" / f"{fname}.json").write_text(safe, encoding="utf-8")
        row = {"name": c["name"], "http": status}
        if status == 200 and isinstance(body, dict):
            row.update(c["parse"](body))
            row["usage"] = body.get("usage") or body.get("usageMetadata")
            note = ""
            if isinstance(row.get("usage"), dict) and "cost" in row["usage"]:
                note = f"coût {row['usage']['cost']} $"
        else:
            row.update(completion_lp=None, prompt_lp=None)
            note = error_message(body)
        row["note"] = scrub(note, secrets)
        summary.append(row)
        fmt = lambda v: "-" if v is None else str(v)  # noqa: E731
        print(f"{c['name']:55} {status:>4} {fmt(row['completion_lp']):>9} "
              f"{fmt(row['prompt_lp']):>9}  {row['note']}")

    (out / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), "utf-8")
    print(f"\nRéponses brutes (sans clés) : {out.relative_to(ROOT)}/raw/")
    print("lp sortie / lp prompt = nombre de tokens avec logprob ; '-' = non applicable ou erreur.")
    print("Pour Mistral, lp prompt = nombre de champs 'prompt_logprob*' non vides trouvés.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
