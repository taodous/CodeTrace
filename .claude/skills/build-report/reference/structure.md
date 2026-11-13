# Structure du rapport de recherche CodeTrace

La template ECE ne fournit que le style. Sa structure (questions T1/E1, « Nom de la partie »,
rappels gris, attestation de binôme) n'est jamais reprise.

## Plan et contenu attendu

| Fichier | Titre | Contenu attendu | Sources |
|---|---|---|---|
| `00-resume` | Résumé / Abstract | 150 à 250 mots chacun : contexte, question, méthode, résultat principal ou état d'avancement, portée. Mots-clés FR/EN. Réécrit à chaque version. | tout le rapport |
| `01-introduction` | Introduction | Contexte et motivations (licences, propriété intellectuelle, fuites de secrets, contamination des benchmarks, pédagogie) ; question de recherche et hypothèses ; contributions **réalisées** ; plan du rapport. | `CLAUDE.md`, `notes/journal.md` |
| `02-etat-de-l-art` | État de l'art | MIA sur LLM (loss, zlib, référence, voisins, Min-K%, Min-K%++) ; critique méthodologique (biais temporel, baselines aveugles, niveau jeu de données) ; travaux sur le code ; accès boîte noire ; tatouage ; positionnement de CodeTrace. Se termine par la lacune visée. | `notes/etat_de_l_art.md`, fiches `notes/*.md`, `notes/related_work.md` |
| `03-cadre` | Cadre formel et modèle de menace | Définition formelle (modèle, extrait, score, seuil) ; niveaux échantillon et jeu de données ; accès par modèle (logprobs prompt ou complétion) avec source et date. | `docs/model_access.md` |
| `04-donnees` | Données | Corpus, licences, langages ; **obtention des labels membre/non-membre** ; nettoyage et déduplication ; contrôle du biais temporel. | `data/README.md`, `src/codetrace/data/`, `notes/decisions.md` |
| `05-methodes` | Méthodes | Perturbations (et garanties de préservation sémantique) ; définitions mathématiques des scores ; comparaison authentique contre perturbé ; critères de décision. | `src/codetrace/perturb/`, `src/codetrace/attacks/` |
| `06-protocole` | Protocole expérimental | Modèles et versions exactes ; métriques (AUC-ROC, TPR à 1 % et 5 % de FPR, IC bootstrap) ; tests (Wilcoxon, permutation) ; baselines dont la baseline aveugle ; seeds, cache, coût. | `experiments/`, `src/codetrace/eval/`, `docs/model_access.md` |
| `07-resultats` | Résultats | Tableaux et figures générés uniquement. Chaque tableau/figure annoncé et commenté. Pas d'interprétation longue (elle va en discussion). | `results/` via `generated/` |
| `08-discussion` | Discussion et limites | Interprétation au regard de la question ; menaces à la validité (interne, externe, de construction) ; réserves du subagent stats-reviewer. | résultats, `notes/decisions.md` |
| `09-outil` | Outil interactif | Architecture, usage, captures. | `app/` |
| `10-conclusion` | Conclusion et perspectives | Ce qui est établi, puis perspectives concrètes et datées si possible. | journal |
| `annexes/A-decisions` | Décisions méthodologiques | Toutes les entrées de `notes/decisions.md` : date, décision, justification, alternatives écartées. | `notes/decisions.md` |
| `annexes/B-reproductibilite` | Reproductibilité | Tableau run / config / commit / seed pour chaque résultat cité ; commit de base de la version. | `version.json`, `experiments/`, `results/*/` |
| `annexes/C-historique` | Historique des versions | Une sous-section par version, la plus récente en tête. | `CHANGELOG.md` |
| `annexes/D-exemples-perturbations` | Exemples de perturbations | Extraits courts authentique et perturbé côte à côte (`listings` dans une figure). | `src/codetrace/perturb/`, tests |

Ajouter une section : nouveau fichier `sections/NN-nom.tex` (le numéro fixe l'ordre). Ne pas
renuméroter les fichiers existants sans raison : les labels `sec:` restent stables.

## Table source -> section (utilisée par `build_report.py delta`)

| Source modifiée | Sections à revoir |
|---|---|
| `notes/etat_de_l_art.md`, `notes/related_work.md` | 02 |
| nouvelle fiche `notes/<papier>.md` | 02 (et 05 si la méthode est reprise) ; lever les `\averifier` correspondants |
| `notes/decisions.md` | annexe A + la section que la décision concerne |
| `notes/journal.md` | 01 (contributions), 10 (perspectives) |
| `docs/model_access.md` | 03, 06 |
| `data/`, `src/codetrace/data/` | 04 |
| `src/codetrace/perturb/` | 05, annexe D |
| `src/codetrace/attacks/` | 05 |
| `src/codetrace/models/` | 03, 06 |
| `src/codetrace/eval/` | 06 |
| `experiments/` | 06, annexe B |
| `results/` | 07, 08, annexe B (et résumé, conclusion) |
| `app/` | 09 |
| `papers/papers.toml` | `refs.bib`, 02 |
| `CLAUDE.md` | 01 |

## Labels
`sec:` pour les sections, `fig:` figures, `tab:` tableaux, `eq:` équations, `ann:` annexes.
Format : `fig:<section>-<objet>` (ex. `fig:resultats-roc-llama`).
