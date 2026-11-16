# TODO CodeTrace

Document vivant : cocher, ajouter, réordonner au fil du projet. Dernière mise à jour : 2026-11-16
(refonte après le meeting tuteur : abandon du double workflow R/P, trois étapes séquentielles).

Rappels CLAUDE.md : aucun chiffre cité sans fiche dans `notes/` ; chaque décision va dans
`notes/decisions.md`.

---

## Étape 1 (immédiate) : au moins 10 papiers lus

« Lu » = lecture complète + fiche dans `notes/` via `/new-paper <chemin PDF>`.
Sélection faite pour couvrir toutes les familles de techniques actuelles (une famille par papier,
le survey sert de carte d'ensemble). Déjà fichés et donc acquis : `mattern2023` (voisinage perturbé)
et `maity2026` (papier des encadrants).

- [x] 1. `contamination/tong2026-pretraining-data-exposure` : survey récent (MIA + contamination +
      sécurité), taxonomie des stratégies de détection. À lire en premier : sert de squelette au tableau.
- [ ] 2. `mia-scores-logprobs/zhang2025-min-k-plus-plus` : scores directs sur logprobs
      (loss, zlib, Min-K%, Min-K%++), ses tableaux comparent aussi Neighbor et référence.
- [ ] 3. `mia-scores-logprobs/xie2024-recall` : calibration par conditionnement (préfixe non-membre).
- [ ] 4. `mia-scores-logprobs/maini2024-dataset-inference` : agrégation de MIA faibles au niveau
      d'un ensemble (dépôt, dataset) + test statistique.
- [ ] 5. `mia-boite-noire/hallinan2025-ngram-coverage` : boîte noire, sans logprobs (texte généré
      seulement), cas des API fermées.
- [ ] 6. `mia-evaluation/duan2024-do-mias-work` : limites et biais d'évaluation (MIMIR, biais temporel).
- [ ] 7. `mia-code/li2025-ai-coders-snitches` (CodeSnitch) : benchmark des MIA sur LLM de code.
- [ ] 8. `mia-code/koohestani2026-ast-pac` : voisinage perturbé adapté au code (perturbations AST).
- [ ] 9. `mia-code/yang2025-equivalent-transformations-mia` : effet des transformations
      sémantiquement équivalentes sur la détection (robustesse, évasion).
- [ ] 10. `watermarking/du2025-sok-copyright-auditing` : approches proactives (watermarks, canaris)
      et cadre intrusif / non intrusif.

Option si un trou apparaît dans le tableau : `mia-code/li2026-synprune` (score syntax-aware),
`mia-boite-noire/duarte2024-de-cop` (QCM boîte noire), `contamination/oren2023-proving-contamination`
(test d'échangeabilité).

## Étape 2 : état de l'art finalisé (définitions + avantages des techniques actuelles)

Pas d'état de l'art extensif : une vraie définition de chaque technique actuelle et de ses avantages.

- [ ] 2a. Tableau comparatif des techniques présentes dans les articles (à faire AVANT la rédaction).
      Colonnes proposées : technique, famille, papier(s), accès requis (logprobs du prompt / texte
      généré / poids / marquage préalable), niveau (extrait / dataset), principe, avantages, limites,
      testé sur du code (oui / non), applicable aux API fermées (oui / non).
- [ ] 2b. Rédiger l'état de l'art à partir du tableau (repartir de `notes/etat_de_l_art.md` et
      `notes/mini_etat_de_l_art_checkpoint.md`).

## Étape 3 : diagramme de Gantt des étapes suivantes (sur Notion)

- [ ] 3a. Lister les étapes post état de l'art (accès modèles, dataset, scores, perturbations,
      évaluation, outil interactif, rapport) avec durées et dépendances.
- [ ] 3b. Construire le Gantt dans Notion (base de données avec vue timeline).

Ensuite seulement : passer à la suite (implémentation).
