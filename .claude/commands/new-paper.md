Utilise le subagent lit-reviewer sur le papier suivant : $ARGUMENTS

Si le papier n'est pas déjà dans papers/papers.toml, ajoute-y un bloc [[paper]]
(file, arxiv, title, topic), ajoute la ligne correspondante dans papers/README.md avec sa licence
arXiv, et lance `uv run python scripts/download_papers.py`.

Ensuite, mets à jour notes/related_work.md : ajoute une ligne au tableau comparatif
(méthode, accès requis, modèles testés, données code ou non, meilleure AUC, limite principale).
