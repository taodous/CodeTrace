# V1 (2026-11-14)

Base : commit befd2492a1

## Ajouts
- 00-resume : résumé et abstract décrivant le projet en phase de cadrage (aucune donnée ni résultat).
  Sources : CLAUDE.md, notes/journal.md.
- 01-introduction : contexte, question de recherche, hypothèse, sept objectifs du sujet,
  contributions réalisées (synthèse préliminaire, cadre, infrastructure), plan. Source : CLAUDE.md.
- 02-etat-de-l-art : six sous-sections rédigées depuis notes/etat_de_l_art.md (MIA sur LLM,
  critique méthodologique, code, boîte noire, tatouage, positionnement).
- 03-cadre : définition formelle (M, x, x̃, s(x, M), τ), niveaux échantillon et jeu de données,
  niveaux d'accès. Tableau d'accès aux modèles laissé en \afaire (docs/model_access.md vide).
- 04-donnees : exigences sur les labels et la baseline aveugle (CLAUDE.md) ; le reste en \afaire.
- 06-protocole : métriques, tests, baselines, reproductibilité et cache (CLAUDE.md).
- 10-conclusion : bilan et prochaines étapes du journal du 2026-11-12.
- Annexes B (commit de base) et C (historique V1).
- refs.bib : 8 papiers de papers/papers.toml + 12 travaux cités dans notes/etat_de_l_art.md
  (das2024, maini2024, meeus2024, li2025, yang2025, yang2024, zhang2023, hallinan2025, yi2026,
  he2025, chauvin2025, sun2023), métadonnées récupérées depuis arXiv.

## Modifications
- Skill build-report, assets/preamble-recherche.tex : correctif \cref / \Cref (le « : » actif de
  babel french cassait les labels sec:x) et tocloft pour élargir les numéros romains dans la table
  des matières (overfull de 6 à 8 pt sur VIII.A, VIII.B).

## Suppressions
- Exclusions volontaires de notes/etat_de_l_art.md : tous les chiffres tirés des papiers
  (taux d'extraction d'Al-Kaswan et al., accuracy de CodeMI, gain d'AUC d'AdvPrompt-MIA,
  nombre de conventions de SynPrune, effet chiffré du renommage, taille des ensembles de Maini et al.)
  ne sont pas repris : aucune fiche de lecture n'existe dans notes/. Les conclusions des papiers
  sont marquées \averifier.
- CoProtector (Sun et al. 2022), TraWiC et DeCoMa ne sont pas dans refs.bib (pas d'identifiant
  dans les notes) : cités sans référence, sous \averifier, ou omis (TraWiC).
- Années bib : on garde l'année du dépôt arXiv (ex. carlini2021 affiché 2020, shi2024 2023) faute
  de fiche confirmant la version publiée en conférence. À corriger lors du fichage.
- 05-methodes, 07, 08, 09, annexes A et D : laissées en \afaire (aucun code, résultat, outil ni
  décision dans le repo).
- notes/related_work.md (tableau vide), data/README.md (aucun dataset) : rien à intégrer au-delà
  des exigences.
