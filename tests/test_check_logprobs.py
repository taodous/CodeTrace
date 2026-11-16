import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "check_logprobs.py"
spec = importlib.util.spec_from_file_location("check_logprobs", SCRIPT)
cl = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cl)


def test_parse_env_ignores_comments_and_empty_values():
    text = '# commentaire\nA_API_KEY=abc\nB_API_KEY=\nC_API_KEY="x y"\n\nnot a line\n'
    assert cl.parse_env(text) == {"A_API_KEY": "abc", "C_API_KEY": "x y"}


def test_scrub_removes_secret_values():
    assert cl.scrub('{"k": "sk-123", "m": "ok"}', ["sk-123", ""]) == '{"k": "***", "m": "ok"}'


def test_count_chat_logprobs():
    resp = {"choices": [{"logprobs": {"content": [{"token": "a", "logprob": -0.1}] * 3}}]}
    assert cl.count_chat_logprobs(resp) == 3
    assert cl.count_chat_logprobs({"choices": [{"logprobs": None}]}) == 0
    assert cl.count_chat_logprobs({}) == 0


def test_count_together_echo():
    resp = {
        "prompt": [{"text": "x", "logprobs": {"tokens": ["a", "b", "c"],
                                              "token_logprobs": [None, -1.0, -2.0]}}],
        "choices": [{"logprobs": {"token_logprobs": [-0.5]}}],
    }
    # le premier token du prompt n'a pas de contexte : logprob None, non compté
    assert cl.count_together_prompt_logprobs(resp) == 2
    assert cl.count_together_completion_logprobs(resp) == 1
    assert cl.count_together_prompt_logprobs({}) == 0


def test_find_prompt_logprobs_nested():
    resp = {"choices": [{"prompt_logprobs": [{"t": -1}]}], "prompt_logprobs_empty": []}
    assert cl.find_prompt_logprobs(resp) == ["choices[0].prompt_logprobs"]


def test_count_gemini_logprobs():
    resp = {"candidates": [{"logprobsResult": {"chosenCandidates": [{}, {}]}}]}
    assert cl.count_gemini_logprobs(resp) == 2
    assert cl.count_gemini_logprobs({"candidates": [{}]}) == 0


def test_build_calls_never_puts_key_in_payload_or_url():
    env = {"OPENROUTER_API_KEY": "SECRET1", "GEMINI_API_KEY": "SECRET2"}
    for c in cl.build_calls(env):
        assert "SECRET" not in c["url"]
        assert "SECRET" not in str(c["payload"])
