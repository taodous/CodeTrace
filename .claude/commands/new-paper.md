Utilise le subagent lit-reviewer sur le papier suivant : $ARGUMENTS

Si le papier n'est pas déjà dans papers/papers.toml, ajoute-y un bloc [[paper]]
(file, arxiv, title, topic), ajoute la ligne correspondante dans papers/README.md avec sa licence
arXiv, et lance `uv run python scripts/download_papers.py`.
Le champ `file` inclut le sous-dossier de catégorie : `file = "<catégorie>/<auteur><année>-<mot-clé>.pdf"`.
Choisis la catégorie dans le tableau « Catégories » de papers/README.md (et incrémente sa colonne Nb) ;
si aucune ne convient, propose-en une nouvelle à l'utilisateur avant de la créer.
Papier hors arXiv : remplace `arxiv` par `url` (lien direct vers le PDF).

Ensuite, mets à jour notes/related_work.md : ajoute une ligne au tableau comparatif
(méthode, accès requis, modèles testés, données code ou non, meilleure AUC, limite principale).
