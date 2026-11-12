"""Télécharge les PDF listés dans papers/papers.toml depuis arXiv.

Usage :
    uv run python scripts/download_papers.py          # télécharge les PDF manquants
    uv run python scripts/download_papers.py --force  # retélécharge tout
"""

import argparse
import sys
import time
import tomllib
import urllib.request
from pathlib import Path

import truststore

# Vérifie les certificats HTTPS avec le magasin du système (Windows, macOS, Linux) au lieu de
# celui de Python : évite CERTIFICATE_VERIFY_FAILED derrière un proxy ou un antivirus.
truststore.inject_into_ssl()

ROOT = Path(__file__).resolve().parent.parent
PAPERS_DIR = ROOT / "papers"
MANIFEST = PAPERS_DIR / "papers.toml"
USER_AGENT = "codetrace-paper-downloader/0.1"


def download(arxiv_id: str, dest: Path) -> None:
    url = f"https://arxiv.org/pdf/{arxiv_id}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = resp.read()
    if not data.startswith(b"%PDF"):
        raise ValueError(f"la réponse de {url} n'est pas un PDF")
    dest.write_bytes(data)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--force", action="store_true", help="retélécharger les PDF existants")
    args = parser.parse_args()

    papers = tomllib.loads(MANIFEST.read_text(encoding="utf-8"))["paper"]
    failures = 0
    for i, paper in enumerate(papers):
        dest = PAPERS_DIR / paper["file"]
        if dest.exists() and not args.force:
            print(f"[deja la] {paper['file']}")
            continue
        if i > 0:
            time.sleep(3)  # politesse envers arXiv
        try:
            download(paper["arxiv"], dest)
            print(f"[ok]      {paper['file']} ({dest.stat().st_size // 1024} Ko)")
        except Exception as e:  # noqa: BLE001
            failures += 1
            print(f"[echec]   {paper['file']} : {e}", file=sys.stderr)

    print(f"\n{len(papers) - failures}/{len(papers)} papiers disponibles dans papers/")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
