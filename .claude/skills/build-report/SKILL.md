---
name: build-report
description: Crée la version suivante du rapport de recherche LaTeX de CodeTrace (report/V{n+1}/) à partir de la template ECE, reprend tout le contenu de la version précédente et y intègre tout ce qui est nouveau dans le repo depuis (notes, fiches, décisions, docs, expériences, résultats, code). À utiliser quand l'utilisateur demande une nouvelle version du rapport, de mettre le rapport à jour, ou tape /build-report.
argument-hint: "[--dry-run] [consigne libre, ex. « focus état de l'art »]"
---

# /build-report : nouvelle version du rapport de recherche

Arguments reçus : `$ARGUMENTS`

Tu produis `report/V{n+1}/`, un rapport de recherche **en français** au style ECE (police,
couleurs, titres, logo de `report/template/rapport-TP-fr.tex`), mais avec une structure de
recherche : la structure TP de la template (T1/E1, rappels gris, attestation de binôme, image
d'électronique) est ignorée. La version contient **tout V{n}** plus **tout ce qui est nouveau**
depuis le commit de base de V{n}.

Lis avant de rédiger :
- `reference/structure.md` : plan du rapport, contenu attendu par section, table source -> section ;
- `reference/style.md` : règles de rédaction scientifique et de typographie LaTeX ;
- `reference/checklist.md` : contrôle qualité final.

Le script `scripts/build_report.py` fait tout ce qui est déterministe (version, copie, manifeste,
delta, export des résultats, contrôles, compilation, diff). Toi, tu lis les sources et tu rédiges.
Ne génère jamais à la main ce que le script sait produire (`main.tex`, `titlepage.tex`,
`preamble-recherche.tex`, `generated/`, `version.json`).

## Étape 0 : pré-vol
```
uv run python scripts/build_report.py status
```
- Outils LaTeX absents (`latexmk`, `biber`) : prévenir l'utilisateur. On peut rédiger, mais la
  version ne sera pas déclarée finie sans compilation. Installation conseillée : TeX Live
  (inclut Perl, nécessaire à latexmk et latexdiff sous Windows), sinon MiKTeX + Strawberry Perl.
- Sources non commitées : s'arrêter et proposer un commit (message à proposer, ne pas commiter
  sans accord). Sans commit, la frontière entre versions n'est pas reproductible.
- `report/report.toml` contient « À compléter » : le signaler (auteurs à renseigner).

## Étape 1 : delta
```
uv run python scripts/build_report.py delta
```
Liste les fichiers modifiés depuis `base_commit` de la dernière version, groupés par section
cible, et les entrées de `notes/journal.md` postérieures. Pour la première version, tout le repo
est « nouveau ». Si la liste est vide et qu'aucune consigne n'est donnée, le dire et ne pas créer
de version.

## Étape 2 : lecture et plan d'intégration
1. Lire **en entier** chaque source listée (et `git diff <base_commit>..HEAD -- <fichier>` pour voir
   ce qui a vraiment changé dans un fichier déjà intégré).
2. Lire les sections de V{n} concernées.
3. Présenter à l'utilisateur un plan court : pour chaque section, ce qui sera ajouté, réécrit ou
   retiré, et pourquoi. Signaler les contradictions entre sources (ex. une décision qui invalide
   un paragraphe de V{n}).
4. Si `$ARGUMENTS` contient `--dry-run` : s'arrêter ici.

## Étape 3 : création de la version
```
uv run python scripts/build_report.py new
```
Crée `report/V{n+1}/` : préambule ECE adapté, page de titre recherche, copie intégrale de
`sections/`, `refs.bib`, `figures/`, `generated/` de V{n} (les retouches manuelles faites dans V{n}
sont donc conservées), `version.json`, `CHANGELOG.md` vide. Ne jamais modifier V{n}.

## Étape 4 : bibliographie
```
uv run python scripts/build_report.py bib                 # papiers de papers/papers.toml
uv run python scripts/build_report.py bib cle=2406.16201  # papier cité hors papers/
```
Clés `auteurAnnée` identiques au préfixe des PDF de `papers/` (`carlini2021`, `zhang2025`...).
Vérifier ensuite dans `refs.bib` : année de publication (conférence plutôt que dépôt arXiv si
connue de la fiche), accents, majuscules protégées. Ne jamais inventer une entrée.

## Étape 5 : résultats (seulement si `results/` a changé)
1. Lancer le subagent **stats-reviewer** sur les nouveaux runs. Ses réserves vont dans
   « Discussion et limites ».
2. ```
   uv run python scripts/build_report.py export-results
   ```
   Convention : `results/<date>_<nom>/metrics.json` (valeurs, IC en liste `[bas, haut]`),
   `tables/*.csv`, `figures/*.pdf|png`, plus la config copiée. Le script génère
   `generated/res-<run>.tex` (macros), `generated/<run>/<table>.tex` (booktabs),
   copie les figures dans `figures/<run>/` et écrit `generated/PROVENANCE.md`.
3. Dans le texte : `\res{<run>}{<cle>}` pour chaque nombre, `\input{generated/<run>/<table>}` dans
   un environnement `table`, figures depuis `figures/<run>/`. **Aucun nombre tapé à la main.**
   Si un run n'a pas de `metrics.json`, ne pas recopier ses chiffres : le signaler.

## Étape 6 : rédaction, section par section
Pour chaque section touchée (ordre du plan) :
- **Intégrer, pas empiler** : réécrire les passages devenus faux ou incomplets pour que la section
  se lise comme un texte unique à jour. Pas de paragraphe « Mise à jour du ... ».
- **Ne rien perdre** : tout contenu de V{n} est conservé sauf s'il est faux ou obsolète ; chaque
  suppression ou correction est consignée dans `CHANGELOG.md` (section « Suppressions » ou
  « Modifications ») avec sa raison.
- **Vérité d'abord** (règles CLAUDE.md) : ne rien affirmer qui ne soit dans le repo. Une section
  sans matière réelle garde ou reçoit `\afaire{ce qui est prévu}`. Un chiffre ou une conclusion
  d'un papier n'est écrit que si une fiche existe dans `notes/` ; sinon citer le travail sans
  chiffre, ou entourer l'affirmation de `\averifier{}`. Tout ce qui est marqué « (web) » dans les
  notes est traité ainsi.
- **Labels membre / non-membre** toujours documentés (source, cutoff, date) dès qu'il y a des données.
- Mettre à jour la ligne de commentaire `% Sources :` en tête du fichier de section si de
  nouvelles sources sont utilisées.
- Une nouvelle section ou annexe : créer `sections/NN-nom.tex` ou `sections/annexes/X-nom.tex` ;
  `main.tex` est régénéré automatiquement par `check` (ordre alphabétique des fichiers).
- Respecter `reference/style.md`.

Toujours, à chaque version :
- **Résumé et abstract** (`00-resume.tex`) réécrits pour refléter l'état réel du projet.
- **Introduction** : la liste des contributions ne contient que ce qui est fait.
- **Annexe A** : toutes les entrées de `notes/decisions.md`.
- **Annexe B** : pour chaque résultat cité, run, config, commit, seed.
- **Annexe C** : ajouter en tête une sous-section `Version n+1 (date)` résumant le CHANGELOG.
- **Conclusion** : perspectives alignées sur les « prochaines étapes » les plus récentes du journal.

## Étape 7 : contrôles et compilation
```
uv run python scripts/build_report.py check
```
Régénère `main.tex`, puis vérifie : tirets cadratins, restes de la template TP, citations absentes
de `refs.bib`, figures et tableaux jamais référencés, nombres en dur dans `07-resultats.tex`,
compilation latexmk + biber, références indéfinies, résultats inconnus, overfull > 5 pt, chktex.
Corriger toutes les **erreurs** et relancer jusqu'à 0 erreur. Traiter les avertissements ou les
justifier dans le résumé final. Puis dérouler `reference/checklist.md`.

## Étape 8 : diff pour les encadrants (à partir de V2)
```
uv run python scripts/build_report.py diff
```
Produit `diff-V{n}-V{n+1}.pdf` (ajouts en bleu, suppressions barrées en rouge).

## Étape 9 : clôture
1. Compléter `CHANGELOG.md` (Ajouts / Modifications / Suppressions, avec les sources) et
   `sections_touched` dans `version.json`.
2. Ajouter une ligne dans `notes/journal.md` à la date du jour : « Rapport V{n+1} généré », sections
   modifiées.
3. Résumer à l'utilisateur : sections modifiées, nombre de `\afaire` et `\averifier` restants,
   avertissements de compilation, chemin du PDF et du diff.
4. Proposer un message de commit (`report/V{n+1}/` + journal) **sans commiter**.
