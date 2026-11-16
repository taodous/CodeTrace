# TODO CodeTrace

Document vivant : cocher, ajouter, réordonner au fil du projet. Dernière mise à jour : 2026-11-15.

## Principe : deux volets menés en parallèle

- **Volet R (recherche)** : lire, ficher, synthétiser, rédiger. Produit : `notes/`, `docs/etat-de-lart/`, `report/`.
- **Volet P (pratique)** : vérifier les accès, coder, expérimenter. Produit : `docs/model_access.md`,
  `src/`, `tests/`, `experiments/`, `results/`.

Règle de couplage : chaque phase associe des lectures à la brique de code qu'elles alimentent
(« → P2 » = cette lecture sert la tâche P2), et chaque résultat pratique revient dans le volet R
(rapport, décisions). On ne lit pas tout avant de coder, et on ne code rien sans avoir lu le papier
qui définit la méthode.

Rappels CLAUDE.md : plan mode avant toute nouvelle expérience ; estimer le coût avant tout run API ;
chaque décision de protocole va dans `notes/decisions.md` ; aucun chiffre cité sans fiche dans `notes/`.

---

## Phase 1 : fondations (maintenant)

Objectif : savoir ce qu'on peut mesurer sur quels modèles, et avoir des scores MIA testés.

### Volet R
- [ ] R1. Envoyer aux encadrants les questions de la fiche Maity (fin de `notes/maity2026-code-provenance.md`) :
      obtention des logprobs d'entrée via OpenRouter, sens de l'inégalité de l'Algorithme 1, lien du dépôt GitHub,
      référence du papier « audit d'API via token probabilities ». Ajouter : le catalogue OpenRouter
      (2026-11-15) n'expose aucun logprob pour GPT-5 ni Gemini 2.5 Flash, ni de logprobs du prompt
      pour aucun modèle (voir `docs/model_access.md`) : comment ont-ils calculé Min-K% ? Demander aussi
      s'il existe un budget API (clés de l'équipe) ou un accès à un cluster GPU de l'ECE. → P1, P4, P11
- [ ] R2. Ficher les papiers qui définissent les scores à implémenter :
      `mia-scores-logprobs/carlini2021-extracting-training-data` (loss, zlib),
      `mia-scores-logprobs/shi2024-min-k-prob` (Min-K%, WikiMIA),
      `mia-scores-logprobs/zhang2025-min-k-plus-plus` (Min-K%++). → P2
- [ ] R3. Ficher les papiers sur la fiabilité de l'évaluation :
      `mia-evaluation/meeus2025-sok-rushing-nowhere`, `mia-evaluation/duan2024-do-mias-work`,
      `mia-evaluation/das2024-blind-baselines`. → P3, P5
- [ ] R4. Ficher les papiers sur l'accès API : `audit-api/chauvin2026-logprob-tracking`,
      `audit-api/gao2025-model-equality-testing` (non-déterminisme des logprobs, provider qui ne sert pas les poids annoncés). → P1

### Volet P
- [ ] P1. **Point critique, restreint aux accès gratuits** (décision du 2026-11-15, voir
      `notes/decisions.md`) : toutes les API du sujet (OpenAI, Google, Mistral, Together, DeepSeek,
      OpenRouter) demandent un paiement. Volet documentaire des API payantes fait, tests réels reportés
      à P11 (si un budget est obtenu, voir R1). À faire maintenant :
      - [ ] P1a. Choisir 2 ou 3 modèles open-weights **dont les données d'entraînement sont publiques**
            (label membre documenté, exigé par CLAUDE.md) et qui tiennent sur la machine (RTX 2050, 4 Go
            de VRAM, 16 Go de RAM : environ 1 à 3B paramètres, 3B en 4 bits). Candidats à vérifier :
            StarCoder2-3B (The Stack v2), Pythia 1.4B/2.8B (The Pile, dont GitHub), OLMo 1B (Dolma).
            Consigner le choix, la licence, le corpus et le cutoff dans `docs/model_access.md`.
      - [ ] P1b. Test réel gratuit : logprobs par token du code d'entrée via transformers en local, sur
            un des modèles de P1a (fusionne avec le début de P4).
      - [ ] P1c. Vérifier les GPU gratuits pour les modèles plus gros (Colab, Kaggle : quotas et VRAM
            réels à relever) et demander aux encadrants si l'ECE a un cluster GPU.
- [ ] P2. `src/codetrace/attacks/` : fonctions pures loss, zlib, Min-K%, Min-K%++ à partir d'un vecteur de
      logprobs par token, avec tests unitaires sur cas jouets (dont le **sens** du score : membre = score haut ?).
- [ ] P3. `src/codetrace/eval/` : AUC-ROC, TPR @ 1 % et 5 % FPR, IC par bootstrap (seed fixée),
      test de permutation ou Wilcoxon pour comparer deux scores. Tests unitaires.
- [ ] P4. `src/codetrace/models/` : wrapper open-weights local (transformers) qui renvoie les logprobs
      par token du texte d'entrée, avec cache disque `.cache/` (clé = modèle + hash). Commencer petit
      (modèle de code de quelques centaines de M à 3B params) pour itérer vite.

### Synchronisation fin de phase 1
- [ ] Consigner dans `notes/decisions.md` : liste des modèles réellement exploitables et par quel accès.
- [ ] Si les API fermées ne donnent pas les logprobs du prompt : décision sur la méthode de repli
      (scorer une complétion, méthodes boîte noire de la phase 3).

---

## Phase 2 : premier protocole propre et reproduction

Objectif : un jeu membres / non-membres au label documenté, et un premier résultat chiffré honnête.

### Volet R
- [ ] R5. Ficher les MIA spécifiques au code : `mia-code/wan2024-code-completion-mia`,
      `mia-code/li2025-ai-coders-snitches`, `mia-code/li2026-synprune`. Noter précisément comment chacun
      construit membres et non-membres. → P5
- [ ] R6. Ficher `contamination/jain2024-livecodebench` et `memorisation/kandpal2022-dedup-privacy`
      (non-membres datés, effet de la déduplication de The Stack). → P5
- [ ] R7. Rédiger dans `docs/etat-de-lart/` une première réponse à la Q2 (questions.md), à partir des fiches R3 et R5.

### Volet P
- [ ] P5. `src/codetrace/data/` : dataset pilote de code. Décider (et consigner) la source du label :
      corpus d'entraînement public connu (ex. The Stack pour un modèle qui l'a utilisé) contre code postérieur
      au cutoff ; ou fine-tuning contrôlé d'un petit modèle (membres garantis). Déduplication.
- [ ] P6. **Baselines obligatoires** sur ce dataset : classifieur sans modèle (Das et al.) et classifieur
      temporel (vieux code contre code récent). Si elles séparent bien les classes, le dataset est biaisé.
- [ ] P7. Reproduire Maity et al. en petit, sur un modèle open-weights : Min-K% avec leurs non-membres
      synthétiques, contre des non-membres naturels. Mesure directe du biais de distribution suspecté.
- [ ] P8. Premier run (plan mode d'abord) : loss, zlib, Min-K%, Min-K%++ sur le dataset pilote,
      résultats dans `results/<date>_<nom>/` avec config copiée, puis relecture par l'agent stats-reviewer.

### Synchronisation fin de phase 2
- [ ] `/build-report` : V2 avec état de l'art enrichi des fiches et premier protocole.
      Avant : régler les clés BibTeX en double (zhang2025 ×3, li2025, yang2024, zhou2025).

---

## Phase 3 : le cœur de CodeTrace (authentique contre perturbé)

### Volet R
- [ ] R8. Ficher `mia-code/yang2025-equivalent-transformations-mia` (contrepoint direct),
      `mia-code/koohestani2026-ast-pac`, `mia-scores-logprobs/mattern2023-neighbourhood-comparison`,
      `mia-code/jiang2025-advprompt-mia-code`. → P9, P10
- [ ] R9. Ficher les méthodes boîte noire si P1 l'impose : `mia-boite-noire/hallinan2025-ngram-coverage`,
      `mia-boite-noire/duarte2024-de-cop`, `mia-code/majdinasab2024-trawic`. → P11
- [ ] R10. Rédiger la réponse à la Q1 (watermarking : à inclure ou non, et comment le positionner)
      à partir de `papers/watermarking/` (au minimum `du2025-sok-copyright-auditing`, `qu2025-repomark`,
      `meeus2024-copyright-traps`).

### Volet P
- [ ] P9. `src/codetrace/perturb/` : perturbations sémantiquement équivalentes (renommage, reformatage,
      réordonnancement, commentaires), chacune testée (le code perturbé s'exécute ou se parse encore).
- [ ] P10. Score de comparaison authentique contre perturbé (type voisinage), évalué contre les scores de P8
      avec test statistique.
- [ ] P11. Extension aux modèles API selon les décisions de fin de phase 1 (estimation de coût d'abord).

---

## Phase 4 : analyse, outil, rédaction finale

### Volet R
- [ ] R11. Rédiger la Q3 (constats solides et zones ouvertes) et situer la contribution de CodeTrace.
- [ ] R12. Sections résultats et discussion du rapport, chaque chiffre relié à `results/`.

### Volet P
- [ ] P12. Critères de décision par modèle et par type de code ; analyse des facteurs (taille, architecture,
      caractéristiques du code).
- [ ] P13. Outil interactif dans `app/` (choix Streamlit ou Gradio à consigner dans decisions.md).

---

## Fait

- [x] 2026-11-14 : questions de l'état de l'art et 70 sources vérifiées (`docs/etat-de-lart/`).
- [x] 2026-11-14 : 70 PDF téléchargés ; 2026-11-15 : classés en 8 catégories (`papers/README.md`).
- [x] 2026-11-14 : rapport V1 (cadrage, état de l'art préliminaire).
- [x] 2026-11-15 : fiche `notes/maity2026-code-provenance.md` + ligne dans `notes/related_work.md`.
