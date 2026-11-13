"""Partie déterministe du skill /build-report : versions du rapport LaTeX de CodeTrace.

Usage :
    uv run python scripts/build_report.py <commande>

    status          dernière version, arbre git, outils LaTeX
    delta           sources modifiées depuis la dernière version, groupées par section
    new             crée report/V{n+1}/ (template ECE adaptée + contenu de V{n})
    bib             ajoute à refs.bib les papiers de papers.toml (+ cle=arxivid)
    export-results  results/ -> generated/ (macros, tableaux) et figures/
    check           régénère main.tex, contrôles statiques, compilation latexmk
    diff            PDF latexdiff V{n-1} -> V{n}

Par défaut les commandes agissent sur la dernière version (option --version N pour une autre).
La rédaction (intégration du contenu) est faite par Claude en suivant
.claude/skills/build-report/SKILL.md ; ce script ne fait que ce qui doit être reproductible.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
import shutil
import subprocess
import sys
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORT = ROOT / "report"
TEMPLATE_DIR = REPORT / "template"
TEMPLATE = TEMPLATE_DIR / "rapport-TP-fr.tex"
METADATA = REPORT / "report.toml"
ASSETS = ROOT / ".claude" / "skills" / "build-report" / "assets"
RESULTS = ROOT / "results"
MANIFEST_NAME = "version.json"

# Sources du rapport, surveillées pour calculer le delta entre deux versions.
SOURCE_PATHS = [
    "CLAUDE.md",
    "notes",
    "docs",
    "data/README.md",
    "papers/papers.toml",
    "src",
    "experiments",
    "results",
    "app",
]

# Préfixe de chemin -> sections cibles. Le premier préfixe qui correspond gagne.
SECTION_MAP: list[tuple[str, list[str]]] = [
    ("notes/etat_de_l_art.md", ["02-etat-de-l-art"]),
    ("notes/related_work.md", ["02-etat-de-l-art"]),
    ("notes/decisions.md", ["annexes/A-decisions", "section concernée par la décision"]),
    ("notes/journal.md", ["01-introduction", "10-conclusion"]),
    ("notes/", ["02-etat-de-l-art (fiche de lecture)"]),
    ("docs/model_access.md", ["03-cadre", "06-protocole"]),
    ("docs/", ["selon le contenu"]),
    ("data/", ["04-donnees"]),
    ("src/codetrace/data", ["04-donnees"]),
    ("src/codetrace/perturb", ["05-methodes", "annexes/D-exemples-perturbations"]),
    ("src/codetrace/attacks", ["05-methodes"]),
    ("src/codetrace/models", ["03-cadre", "06-protocole"]),
    ("src/codetrace/eval", ["06-protocole"]),
    ("src/", ["selon le contenu"]),
    ("experiments/", ["06-protocole", "annexes/B-reproductibilite"]),
    ("results/", ["07-resultats", "08-discussion", "annexes/B-reproductibilite"]),
    ("app/", ["09-outil"]),
    ("papers/papers.toml", ["refs.bib", "02-etat-de-l-art"]),
    ("CLAUDE.md", ["01-introduction"]),
]

LATEX_TOOLS = ["latexmk", "pdflatex", "biber", "latexdiff", "chktex"]
MOIS = [
    "janvier",
    "février",
    "mars",
    "avril",
    "mai",
    "juin",
    "juillet",
    "août",
    "septembre",
    "octobre",
    "novembre",
    "décembre",
]


# --------------------------------------------------------------------------- utilitaires


def git(*args: str) -> str:
    out = subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", check=True
    )
    return out.stdout


def rel(path: Path) -> str:
    """Chemin lisible : relatif au repo si possible."""
    path = Path(path).resolve()
    return path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else path.as_posix()


def list_versions(report_dir: Path = REPORT) -> list[int]:
    if not report_dir.exists():
        return []
    nums = [
        int(m.group(1))
        for p in report_dir.iterdir()
        if p.is_dir() and (m := re.fullmatch(r"V(\d+)", p.name))
    ]
    return sorted(nums)


def version_dir(n: int, report_dir: Path = REPORT) -> Path:
    return report_dir / f"V{n}"


def load_manifest(vdir: Path) -> dict | None:
    path = vdir / MANIFEST_NAME
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def date_longue(d: dt.date) -> str:
    jour = "1er" if d.day == 1 else str(d.day)
    return f"{jour} {MOIS[d.month - 1]} {d.year}"


def latex_escape(text: str) -> str:
    repl = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    return "".join(repl.get(c, c) for c in text)


def strip_comments(tex: str) -> str:
    """Retire les commentaires LaTeX (un % non échappé et la suite de la ligne)."""
    return "\n".join(re.sub(r"(?<!\\)%.*", "", line) for line in tex.splitlines())


def section_targets(path: str) -> list[str]:
    for prefix, targets in SECTION_MAP:
        if path == prefix or path.startswith(prefix):
            return targets
    return ["selon le contenu"]


# --------------------------------------------------------------------------- template


def split_template(template: str) -> tuple[str, str]:
    marker = r"\begin{document}"
    idx = template.find(marker)
    if idx < 0:
        raise ValueError("la template ne contient pas \\begin{document}")
    return template[:idx], template[idx:]


def adapt_preamble(preamble: str, version: int, meta: dict) -> str:
    """Garde le préambule ECE et remplace uniquement ce qui est spécifique au TP."""
    header = rf"\fancyhead[R]{{\textcolor{{ece}}{{{meta['titre']}}} \textbullet{{}} V{version}}}"
    preamble, n = re.subn(r"\\fancyhead\[R\]\{[^\n]*", lambda _: header, preamble)
    if n != 1:
        raise ValueError("en-tête droit (\\fancyhead[R]) introuvable dans la template")
    titre = f"{meta['titre']} : {meta['sous_titre']}"
    auteurs = ", ".join(meta["auteurs"])
    extra = (
        "\n% ---------------------------------------------------------------------\n"
        "% Ajouts recherche (build_report.py).\n"
        "% Le préambule ci-dessus est celui de la template ECE.\n"
        "\\input{preamble-recherche}\n"
        f"\\hypersetup{{pdftitle={{{titre}}}, pdfauthor={{{auteurs}}}, pdflang={{fr}}}}\n\n"
    )
    return preamble.rstrip() + "\n" + extra


def build_body(sections: list[str], annexes: list[str]) -> str:
    lines = [r"\begin{document}", "", r"\input{titlepage}", ""]
    main = [s for s in sections if s != "00-resume"]
    if "00-resume" in sections:
        lines += [r"\input{sections/00-resume}", ""]
    lines += [r"\tableofcontents", r"\newpage", ""]
    lines += [rf"\input{{sections/{s}}}" for s in main]
    lines += ["", r"\newpage", r"\printbibliography[heading=bibintoc, title={Références}]", ""]
    if annexes:
        lines += [r"\newpage", r"\appendix"]
        lines += [rf"\input{{sections/annexes/{a}}}" for a in annexes]
    lines += ["", r"\end{document}", ""]
    return "\n".join(lines)


def render_main(template: str, version: int, meta: dict, vdir: Path) -> str:
    preamble, _ = split_template(template)
    sections = sorted(p.stem for p in (vdir / "sections").glob("*.tex"))
    annexes = sorted(p.stem for p in (vdir / "sections" / "annexes").glob("*.tex"))
    head = (
        "% Fichier GÉNÉRÉ par scripts/build_report.py depuis report/template/rapport-TP-fr.tex.\n"
        "% Ne pas éditer : modifier sections/, report/report.toml ou la template, puis `check`.\n"
    )
    return head + adapt_preamble(preamble, version, meta) + build_body(sections, annexes)


def render_titlepage(asset: str, version: int, meta: dict, date: dt.date) -> str:
    values = {
        "TYPE": meta["type_document"],
        "TITRE": meta["titre"],
        "SOUS_TITRE": meta["sous_titre"],
        "ANNEE": meta["annee"],
        "VERSION": str(version),
        "DATE_LONGUE": date_longue(date),
        "AUTEURS": r" \\ ".join(meta["auteurs"]),
        "ENCADRANTS": r" \\ ".join(meta["encadrants"]),
        "EQUIPE": meta["equipe"],
        "VILLE": meta["ville"],
    }
    for key, val in values.items():
        asset = asset.replace("{{" + key + "}}", val)
    if left := re.findall(r"\{\{[A-Z_]+\}\}", asset):
        raise ValueError(f"variable(s) de page de titre non remplacée(s) : {left}")
    return asset


def load_meta() -> dict:
    return tomllib.loads(METADATA.read_text(encoding="utf-8"))


def write_main(vdir: Path, version: int, date: dt.date) -> None:
    meta = load_meta()
    template = TEMPLATE.read_text(encoding="utf-8")
    (vdir / "main.tex").write_text(render_main(template, version, meta, vdir), encoding="utf-8")
    asset = (ASSETS / "titlepage.tex").read_text(encoding="utf-8")
    (vdir / "titlepage.tex").write_text(
        render_titlepage(asset, version, meta, date), encoding="utf-8"
    )
    shutil.copy2(ASSETS / "preamble-recherche.tex", vdir / "preamble-recherche.tex")


# --------------------------------------------------------------------------- delta


@dataclass
class Delta:
    base_commit: str | None
    changed: list[tuple[str, str]] = field(default_factory=list)  # (statut, chemin)
    dirty: list[str] = field(default_factory=list)
    journal: list[str] = field(default_factory=list)


def dirty_sources() -> list[str]:
    out = git("status", "--porcelain", "--untracked-files=all", "--", *SOURCE_PATHS)
    return [line[3:].strip().strip('"') for line in out.splitlines() if line.strip()]


def journal_entries_since(text: str, since: dt.date | None) -> list[str]:
    heads = re.findall(r"^##\s+(\d{4}-\d{2}-\d{2})", text, flags=re.M)
    return [h for h in heads if since is None or dt.date.fromisoformat(h) >= since]


def is_trivial(path: str, root: Path = ROOT) -> bool:
    """Fichiers sans contenu à rapporter : .gitkeep et fichiers vides (ex. __init__.py)."""
    if Path(path).name == ".gitkeep":
        return True
    f = root / path
    return f.is_file() and not f.read_bytes().strip()


def compute_delta(manifest: dict | None) -> Delta:
    base = manifest["base_commit"] if manifest else None
    delta = Delta(base_commit=base)
    if base:
        out = git("diff", "--name-status", f"{base}..HEAD", "--", *SOURCE_PATHS)
        for line in out.splitlines():
            parts = line.split("\t")
            delta.changed.append((parts[0], parts[-1]))
    else:
        delta.changed = [("A", p) for p in git("ls-files", "--", *SOURCE_PATHS).splitlines()]
    delta.changed = [(s, p) for s, p in delta.changed if not is_trivial(p)]
    delta.dirty = dirty_sources()
    journal = ROOT / "notes" / "journal.md"
    if journal.exists():
        since = dt.date.fromisoformat(manifest["date"]) if manifest else None
        delta.journal = journal_entries_since(journal.read_text(encoding="utf-8"), since)
    return delta


# --------------------------------------------------------------------------- export des résultats


def sanitize_key(key: str) -> str:
    return re.sub(r"[^A-Za-z0-9.-]", "-", key)


def flatten(obj, prefix: str = "") -> dict[str, object]:
    if isinstance(obj, dict):
        out: dict[str, object] = {}
        for k, v in obj.items():
            out.update(flatten(v, f"{prefix}.{k}" if prefix else str(k)))
        return out
    return {prefix: obj}


def format_value(v: object) -> str:
    if isinstance(v, bool):
        return "oui" if v else "non"
    if isinstance(v, int | float):
        return rf"\num{{{v}}}"
    if isinstance(v, list) and len(v) == 2 and all(isinstance(x, int | float) for x in v):
        return rf"[\num{{{v[0]}}}~; \num{{{v[1]}}}]"  # intervalle de confiance
    return latex_escape(str(v))


def metrics_to_tex(run: str, metrics: dict, source: str) -> str:
    lines = [f"% Généré depuis {source} : ne pas éditer."]
    for key, val in flatten(metrics).items():
        lines.append(
            rf"\defres{{{sanitize_key(run)}}}{{{sanitize_key(key)}}}{{{format_value(val)}}}"
        )
    return "\n".join(lines) + "\n"


def csv_to_tex(rows: list[list[str]], source: str) -> str:
    if not rows:
        raise ValueError(f"CSV vide : {source}")
    header, body = rows[0], rows[1:]

    def cell(c: str) -> str:
        try:
            float(c)
            return rf"\num{{{c}}}"
        except ValueError:
            return latex_escape(c)

    lines = [
        f"% Généré depuis {source} : ne pas éditer. À inclure dans un environnement table.",
        r"\begin{tabular}{" + "l" * len(header) + "}",
        r"\toprule",
        " & ".join(rf"\textbf{{{latex_escape(h)}}}" for h in header) + r" \\",
        r"\midrule",
        *(" & ".join(cell(c) for c in row) + r" \\" for row in body),
        r"\bottomrule",
        r"\end{tabular}",
    ]
    return "\n".join(lines) + "\n"


def export_results(vdir: Path, results_dir: Path = RESULTS) -> list[str]:
    gen, figs = vdir / "generated", vdir / "figures"
    gen.mkdir(exist_ok=True)
    log: list[str] = []
    macro_files: list[str] = []
    runs = sorted(p for p in results_dir.iterdir() if p.is_dir()) if results_dir.exists() else []
    for run in runs:
        src = rel(run)
        metrics = run / "metrics.json"
        if metrics.exists():
            name = f"res-{sanitize_key(run.name)}.tex"
            data = json.loads(metrics.read_text(encoding="utf-8"))
            (gen / name).write_text(
                metrics_to_tex(run.name, data, f"{src}/metrics.json"), encoding="utf-8"
            )
            macro_files.append(name)
            log.append(f"{src}/metrics.json -> generated/{name}")
        for table in sorted((run / "tables").glob("*.csv")):
            out = gen / sanitize_key(run.name) / f"{table.stem}.tex"
            out.parent.mkdir(exist_ok=True)
            with table.open(encoding="utf-8", newline="") as f:
                rows = list(csv.reader(f))
            out.write_text(csv_to_tex(rows, f"{src}/tables/{table.name}"), encoding="utf-8")
            log.append(f"{src}/tables/{table.name} -> {out.relative_to(vdir).as_posix()}")
        for fig in sorted((run / "figures").glob("*")):
            if fig.suffix.lower() in {".pdf", ".png", ".jpg", ".jpeg"}:
                dest = figs / sanitize_key(run.name) / fig.name
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(fig, dest)
                log.append(f"{src}/figures/{fig.name} -> {dest.relative_to(vdir).as_posix()}")
    index = ["% Généré par build_report.py export-results : ne pas éditer."]
    index += [rf"\input{{generated/{n.removesuffix('.tex')}}}" for n in macro_files]
    (gen / "resultats.tex").write_text("\n".join(index) + "\n", encoding="utf-8")
    (gen / "PROVENANCE.md").write_text(
        "# Provenance des fichiers générés\n\n" + "".join(f"- {line}\n" for line in log),
        encoding="utf-8",
    )
    return log


# --------------------------------------------------------------------------- contrôles


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    infos: list[str] = field(default_factory=list)


CITE_RE = re.compile(r"\\(?:[a-zA-Z]*cite[a-z]*|citeauthor|citeyear)\*?(?:\[[^\]]*\])*\{([^}]*)\}")
LABEL_RE = re.compile(r"\\label\{((?:fig|tab):[^}]*)\}")
REF_RE = re.compile(r"\\(?:[cC]ref|ref|autoref|crefrange|pageref|vref)\{([^}]*)\}")
LEFTOVERS = [
    r"colorbox{yellow}",
    "RAPPORT DE TP",
    "binôme",
    "elec.png",
    r"\textbf{\textcolor{ece}{T1.}}",
]
NUMBER_RE = re.compile(r"(?<![\w\\{])\d+[.,]\d+")


def static_checks(files: dict[str, str], bib: str) -> Report:
    rep = Report()
    bib_keys = set(re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,", bib))
    cited: set[str] = set()
    labels: dict[str, str] = {}
    refs: set[str] = set()
    afaire = averifier = 0
    for name, raw in files.items():
        tex = strip_comments(raw)
        if "—" in tex or re.search(r"(?<!-)---(?!-)", tex):
            rep.errors.append(f"{name} : tiret cadratin interdit (— ou ---)")
        for bad in LEFTOVERS:
            if bad in tex:
                rep.errors.append(f"{name} : reste de la template TP ({bad})")
        for group in CITE_RE.findall(tex):
            cited.update(k.strip() for k in group.split(",") if k.strip())
        for lab in LABEL_RE.findall(tex):
            labels[lab] = name
        for group in REF_RE.findall(tex):
            refs.update(k.strip() for k in group.split(","))
        afaire += tex.count(r"\afaire{")
        averifier += tex.count(r"\averifier{")
        if name.endswith("07-resultats.tex"):
            for num in NUMBER_RE.findall(re.sub(r"\\res\{[^}]*\}\{[^}]*\}", "", tex)):
                rep.errors.append(
                    f"{name} : nombre en dur « {num} » (utiliser \\res ou generated/)"
                )
        if "À compléter" in tex:
            rep.warnings.append(f"{name} : « À compléter » (voir report/report.toml)")
    for key in sorted(cited - bib_keys):
        rep.errors.append(f"citation sans entrée dans refs.bib : {key}")
    for lab, name in sorted(labels.items()):
        if lab not in refs:
            rep.warnings.append(f"{name} : {lab} n'est jamais référencé dans le texte (\\cref)")
    rep.infos.append(f"marqueurs \\afaire : {afaire}, \\averifier : {averifier}")
    return rep


def parse_latex_log(log: str, overfull_pt: float = 5.0) -> Report:
    rep = Report()
    for m in re.finditer(r"LaTeX Warning: (Reference|Citation) [`']([^']*)' .*undefined", log):
        rep.errors.append(f"{m.group(1).lower()} indéfinie : {m.group(2)}")
    for m in re.finditer(r"Package codetrace Warning: Resultat inconnu: ([^\s]+)", log):
        rep.errors.append(f"résultat inconnu : {m.group(1)}")
    for m in re.finditer(r"Overfull \\hbox \((\d+(?:\.\d+)?)pt too wide\)[^\n]*lines? (\d+)", log):
        if float(m.group(1)) > overfull_pt:
            rep.warnings.append(f"overfull hbox {m.group(1)}pt (ligne {m.group(2)})")
    if "Please (re)run Biber" in log or "Please rerun LaTeX" in log:
        rep.warnings.append("compilation incomplète : relancer")
    return rep


def run_check(vdir: Path, version: int, compile_pdf: bool = True) -> Report:
    manifest = load_manifest(vdir) or {}
    date = dt.date.fromisoformat(manifest.get("date", dt.date.today().isoformat()))
    write_main(vdir, version, date)
    files = {
        p.relative_to(vdir).as_posix(): p.read_text(encoding="utf-8")
        for p in sorted(vdir.rglob("*.tex"))
        if not p.relative_to(vdir).as_posix().startswith(("generated/", "diff"))
    }
    bib_path = vdir / "refs.bib"
    rep = static_checks(files, bib_path.read_text(encoding="utf-8") if bib_path.exists() else "")
    if not compile_pdf:
        return rep
    if not shutil.which("latexmk"):
        rep.errors.append("latexmk introuvable : installer une distribution LaTeX (voir SKILL.md)")
        return rep
    proc = subprocess.run(
        ["latexmk", "-pdf", "-interaction=nonstopmode", "-file-line-error", "main.tex"],
        cwd=vdir,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    log_path = vdir / "main.log"
    log = log_path.read_text(encoding="utf-8", errors="replace") if log_path.exists() else ""
    if proc.returncode != 0:
        errs = re.findall(r"^[^\n]*:\d+: [^\n]*", log, flags=re.M)[:10] or [proc.stdout[-1500:]]
        rep.errors.append("échec de compilation :\n    " + "\n    ".join(errs))
    sub = parse_latex_log(log)
    rep.errors += sub.errors
    rep.warnings += sub.warnings
    blg = vdir / "main.blg"
    if blg.exists():
        for line in blg.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.startswith(("WARN", "ERROR")):
                rep.warnings.append(f"biber : {line}")
    if shutil.which("chktex"):
        out = subprocess.run(
            ["chktex", "-q", "-n1", "-n8", "-n36", "main.tex"],
            cwd=vdir,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        n = len([line for line in out.stdout.splitlines() if line.startswith("Warning")])
        if n:
            rep.infos.append(
                f"chktex : {n} avertissement(s) (lancer `chktex main.tex` pour le détail)"
            )
    return rep


# --------------------------------------------------------------------------- bibliographie


def bib_keys_of(bib: str) -> set[str]:
    return set(re.findall(r"@\w+\s*\{\s*([^,\s]+)\s*,", bib))


def arxiv_entries(ids: dict[str, str]) -> list[str]:
    """ids : clé BibTeX -> identifiant arXiv. Interroge l'API arXiv (un seul appel)."""
    import urllib.parse
    import urllib.request
    import xml.etree.ElementTree as ET

    import truststore

    truststore.inject_into_ssl()
    url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(
        {"id_list": ",".join(ids.values()), "max_results": len(ids)}
    )
    req = urllib.request.Request(url, headers={"User-Agent": "codetrace-report/0.1"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        root = ET.fromstring(resp.read())
    ns = {"a": "http://www.w3.org/2005/Atom", "x": "http://arxiv.org/schemas/atom"}
    by_id: dict[str, ET.Element] = {}
    for entry in root.findall("a:entry", ns):
        aid = re.sub(r"v\d+$", "", entry.findtext("a:id", "", ns).rsplit("/abs/", 1)[-1])
        by_id[aid] = entry
    out = []
    for key, aid in ids.items():
        e = by_id.get(aid)
        if e is None:
            print(f"[absent]  {key} ({aid}) introuvable sur arXiv", file=sys.stderr)
            continue
        title = " ".join(e.findtext("a:title", "", ns).split())
        authors = " and ".join(a.findtext("a:name", "", ns) for a in e.findall("a:author", ns))
        year = e.findtext("a:published", "", ns)[:4]
        prim = e.find("x:primary_category", ns)
        cls = prim.get("term") if prim is not None else ""
        out.append(
            f"@misc{{{key},\n  author = {{{authors}}},\n  title = {{{{{title}}}}},\n"
            f"  year = {{{year}}},\n  eprint = {{{aid}}},\n  eprinttype = {{arxiv}},\n"
            f"  eprintclass = {{{cls}}},\n  url = {{https://arxiv.org/abs/{aid}}},\n}}\n"
        )
    return out


def cmd_bib(vdir: Path, extra: list[str]) -> int:
    bib_path = vdir / "refs.bib"
    bib = bib_path.read_text(encoding="utf-8") if bib_path.exists() else ""
    present = bib_keys_of(bib)
    papers = tomllib.loads((ROOT / "papers" / "papers.toml").read_text(encoding="utf-8"))["paper"]
    wanted = {p["file"].split("-")[0]: p["arxiv"] for p in papers}
    for item in extra:  # forme cle=arxivid
        key, _, aid = item.partition("=")
        wanted[key] = aid
    missing = {k: v for k, v in wanted.items() if k not in present}
    if not missing:
        print("refs.bib est à jour.")
        return 0
    entries = arxiv_entries(missing)
    with bib_path.open("a", encoding="utf-8") as f:
        for e in entries:
            f.write("\n" + e)
    print(f"{len(entries)} entrée(s) ajoutée(s) à {rel(bib_path)} : " + ", ".join(missing))
    return 0 if len(entries) == len(missing) else 1


# --------------------------------------------------------------------------- commandes


def resolve(args) -> tuple[int, Path]:
    versions = list_versions()
    if not versions:
        sys.exit("Aucune version : lancer d'abord `build_report.py new`.")
    n = args.version or versions[-1]
    if n not in versions:
        sys.exit(f"V{n} n'existe pas (versions : {versions}).")
    return n, version_dir(n)


def cmd_status(_args) -> int:
    versions = list_versions()
    print(f"Versions existantes : {', '.join(f'V{v}' for v in versions) or 'aucune'}")
    if versions:
        m = load_manifest(version_dir(versions[-1])) or {}
        print(
            f"Dernière : V{versions[-1]}, date {m.get('date')}, base_commit {m.get('base_commit')}"
        )
    print(f"Prochaine : V{(versions[-1] if versions else 0) + 1}")
    print(f"HEAD : {git('rev-parse', '--short', 'HEAD').strip()}")
    dirty = dirty_sources()
    print(f"Sources non commitées : {len(dirty)}")
    for p in dirty:
        print(f"  {p}")
    for tool in LATEX_TOOLS:
        print(f"{tool:10} {shutil.which(tool) or 'ABSENT'}")
    return 0


def cmd_delta(_args) -> int:
    versions = list_versions()
    manifest = load_manifest(version_dir(versions[-1])) if versions else None
    delta = compute_delta(manifest)
    print(f"Base : {delta.base_commit or 'aucune (première version, tout est nouveau)'}")
    groups: dict[str, list[str]] = {}
    for status, path in delta.changed:
        for target in section_targets(path):
            groups.setdefault(target, []).append(f"{status} {path}")
    for target in sorted(groups):
        print(f"\n[{target}]")
        for line in groups[target]:
            print(f"  {line}")
    if delta.journal:
        print(f"\nEntrées de notes/journal.md à intégrer : {', '.join(delta.journal)}")
    if delta.dirty:
        print("\nATTENTION, sources modifiées non commitées (à commiter avant `new`) :")
        for p in delta.dirty:
            print(f"  {p}")
        return 2
    return 0


def cmd_new(args) -> int:
    dirty = dirty_sources()
    if dirty and not args.allow_dirty:
        print("Sources non commitées : commiter d'abord (ou --allow-dirty) :", file=sys.stderr)
        for p in dirty:
            print(f"  {p}", file=sys.stderr)
        return 2
    versions = list_versions()
    prev = versions[-1] if versions else None
    n = (prev or 0) + 1
    vdir = version_dir(n)
    vdir.mkdir(parents=True)
    today = dt.date.today()
    if prev is None:
        shutil.copytree(ASSETS / "sections", vdir / "sections")
        (vdir / "refs.bib").write_text(
            "% Bibliographie (biblatex/biber). Clés auteurAnnée.\n", encoding="utf-8"
        )
        prev_manifest = None
    else:
        pdir = version_dir(prev)
        for name in ("sections", "generated", "figures"):
            if (pdir / name).exists():
                shutil.copytree(pdir / name, vdir / name)
        if (pdir / "refs.bib").exists():
            shutil.copy2(pdir / "refs.bib", vdir / "refs.bib")
        prev_manifest = load_manifest(pdir)
    (vdir / "images").mkdir(exist_ok=True)
    shutil.copy2(TEMPLATE_DIR / "images" / "ece.png", vdir / "images" / "ece.png")
    write_main(vdir, n, today)
    delta = compute_delta(prev_manifest)
    manifest = {
        "version": n,
        "date": today.isoformat(),
        "base_commit": git("rev-parse", "HEAD").strip(),
        "previous": prev,
        "previous_commit": prev_manifest["base_commit"] if prev_manifest else None,
        "dirty_sources": delta.dirty,
        "sources_changed": [p for _, p in delta.changed],
        "sections_touched": [],
    }
    (vdir / MANIFEST_NAME).write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    changelog = (
        f"# V{n} ({today.isoformat()})\n\n"
        f"Base : commit {manifest['base_commit'][:10]}"
        + (f", depuis V{prev} (commit {manifest['previous_commit'][:10]})" if prev else "")
        + "\n\n## Ajouts\n\n## Modifications\n\n## Suppressions\n"
    )
    (vdir / "CHANGELOG.md").write_text(changelog, encoding="utf-8")
    print(
        f"Créé : {rel(vdir)}",
        f"(depuis {'V' + str(prev) if prev else 'la template'})",
    )
    print(
        f"{len(manifest['sources_changed'])} source(s) à intégrer : lancer `delta` pour le détail."
    )
    return 0


def print_report(rep: Report) -> int:
    for e in rep.errors:
        print(f"ERREUR    {e}")
    for w in rep.warnings:
        print(f"ATTENTION {w}")
    for i in rep.infos:
        print(f"INFO      {i}")
    print(f"\n{len(rep.errors)} erreur(s), {len(rep.warnings)} avertissement(s).")
    return 1 if rep.errors else 0


def cmd_check(args) -> int:
    n, vdir = resolve(args)
    return print_report(run_check(vdir, n, compile_pdf=not args.no_compile))


def cmd_export(args) -> int:
    _, vdir = resolve(args)
    log = export_results(vdir)
    print("\n".join(log) if log else "Aucun fichier exploitable dans results/.")
    return 0


def cmd_diff(args) -> int:
    n, vdir = resolve(args)
    if n == 1:
        print("V1 : pas de version précédente.")
        return 0
    pdir = version_dir(n - 1)
    for tool in ("latexdiff", "latexmk"):
        if not shutil.which(tool):
            print(f"{tool} introuvable.", file=sys.stderr)
            return 1
    out = subprocess.run(
        [
            "latexdiff",
            "--flatten",
            "--encoding=utf8",
            str(pdir / "main.tex"),
            str(vdir / "main.tex"),
        ],
        capture_output=True,
        text=True,
        encoding="utf-8",
        cwd=vdir,
    )
    if out.returncode != 0:
        print(out.stderr, file=sys.stderr)
        return 1
    name = f"diff-V{n - 1}-V{n}"
    (vdir / f"{name}.tex").write_text(out.stdout, encoding="utf-8")
    comp = subprocess.run(
        ["latexmk", "-pdf", "-interaction=nonstopmode", f"{name}.tex"],
        cwd=vdir,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if comp.returncode != 0:
        print(f"Compilation de {name}.tex en échec (voir {name}.log).", file=sys.stderr)
        return 1
    print(f"Créé : {rel(vdir / f'{name}.pdf')}")
    return 0


def main(argv: list[str] | None = None) -> int:
    for stream in (sys.stdout, sys.stderr):  # console Windows : accents lisibles
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status")
    sub.add_parser("delta")
    p_new = sub.add_parser("new")
    p_new.add_argument("--allow-dirty", action="store_true")
    p_bib = sub.add_parser("bib")
    p_bib.add_argument("extra", nargs="*", help="entrées supplémentaires cle=arxivid")
    p_bib.add_argument("--version", type=int)
    for name in ("export-results", "check", "diff"):
        p = sub.add_parser(name)
        p.add_argument("--version", type=int)
        if name == "check":
            p.add_argument("--no-compile", action="store_true")
    args = parser.parse_args(argv)
    if args.cmd == "bib":
        return cmd_bib(resolve(args)[1], args.extra)
    handlers = {
        "status": cmd_status,
        "delta": cmd_delta,
        "new": cmd_new,
        "check": cmd_check,
        "export-results": cmd_export,
        "diff": cmd_diff,
    }
    return handlers[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
