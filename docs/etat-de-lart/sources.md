# Sources pour les questions de l'état de l'art

Questions : voir [questions.md](questions.md). Ce fichier **ne répond pas** aux questions : il liste les
sources qui permettent d'y répondre et dit, pour chacune, quel aspect elle éclaire.

## Méthode et niveau de vérification (2026-11-14)

- Recherche faite par trois sous-agents (un par question), puis fusion et dédoublonnage : **70 sources uniques**.
- Vérification en deux temps :
  1. chaque sous-agent a ouvert la page de la source (arxiv.org/abs, aclanthology.org, usenix.org, proceedings) ;
  2. recontrôle de toutes les sources le 2026-11-14 : les 68 identifiants arXiv via l'API arXiv
     (titre, premier auteur, date, champ comments/journal-ref), les 3 pages ACL Anthology via leur
     BibTeX, la page USENIX via son titre. **Les 70 correspondent.**
- Ce qui n'a **pas** été fait : aucune lecture intégrale. Les descriptions viennent des abstracts seulement.
  Conformément à CLAUDE.md, rien ici ne doit être cité comme résultat avant d'avoir une fiche dans notes/.
- Colonne « Venue » : telle qu'affichée par la page (comments arXiv, journal-ref, BibTeX). « arXiv » = aucun
  venue affiché. Les venues signalées par ⚠ ne sont pas confirmées (voir la section dédiée en bas).

## Tableau de synthèse

Légende : ● = source principale pour la question, ○ = utile en appui. Code : la source porte sur du code.
BN (boîte noire) : oui = sorties seules, partiel = logprobs de complétion ou modèles substituts, non = logprobs
du texte d'entrée ou accès aux poids. « papers/ » : PDF déjà présent dans le repo.

| # | id | Référence | Année | Venue | Lien | Q1 | Q2 | Q3 | Code | BN | papers/ |
|---|----|-----------|-------|-------|------|----|----|----|------|----|---------|
| 1 | sun2022-coprotector | Sun et al., CoProtector | 2021 | WWW 2022 | [2110.12925](https://arxiv.org/abs/2110.12925) | ● | | | oui | | |
| 2 | sun2023-codemark | Sun et al., CodeMark | 2023 | FSE 2023 | [2308.14401](https://arxiv.org/abs/2308.14401) | ● | | | oui | | |
| 3 | xiao2025-decoma | Xiao et al., DeCoMa | 2025 | ISSTA 2025 | [2504.07002](https://arxiv.org/abs/2504.07002) | ● | | | oui | | |
| 4 | chen2026-ducodemark | Chen et al., DuCodeMark | 2026 | FSE 2026 | [2604.10611](https://arxiv.org/abs/2604.10611) | ● | | | oui | | |
| 5 | qu2025-repomark | Qu et al., RepoMark | 2025 | arXiv | [2508.21432](https://arxiv.org/abs/2508.21432) | ● | | | oui | | |
| 6 | meeus2024-copyright-traps | Meeus et al., Copyright Traps for LLMs | 2024 | ICML 2024 | [2402.09363](https://arxiv.org/abs/2402.09363) | ● | ○ | | | non | |
| 7 | wei2024-data-watermarks | Wei et al., Proving membership via data watermarks | 2024 | Findings ACL 2024 | [2402.10892](https://arxiv.org/abs/2402.10892) | ● | | | | oui | |
| 8 | rastogi2025-stamp | Rastogi et al., STAMP | 2025 | ICML 2025 | [2504.13416](https://arxiv.org/abs/2504.13416) | ● | | | | | |
| 9 | li2025-provenance-unicode | Li et al., Data Provenance Auditing of Fine-Tuned LLMs | 2025 | ICML 2026 | [2510.09655](https://arxiv.org/abs/2510.09655) | ○ | | | | oui | |
| 10 | weinberg2026-sigil | Weinberg, Subtle Injection for Ground-truth Inference | 2026 | arXiv | [2606.06502](https://arxiv.org/abs/2606.06502) | ○ | | | partiel | | |
| 11 | du2025-sok-copyright-auditing | Du et al., SoK: Dataset Copyright Auditing | 2024 | IEEE S&P 2025 | [2410.16618](https://arxiv.org/abs/2410.16618) | ● | | | | | |
| 12 | liu2026-implicit-identity | Liu et al., Implicit Identity Technologies for LLMs | 2026 | IJCAI-ECAI 2026 | [2605.29245](https://arxiv.org/abs/2605.29245) | ○ | | | | | |
| 13 | sander2024-radioactive | Sander et al., Watermarking Makes LMs Radioactive | 2024 | NeurIPS 2024 | [2402.14904](https://arxiv.org/abs/2402.14904) | ○ | | | | | |
| 14 | jovanovic2025-ward | Jovanović et al., Ward | 2024 | ICLR 2025 | [2410.03537](https://arxiv.org/abs/2410.03537) | ○ | | | | | |
| 15 | meeus2025-sok-rushing-nowhere | Meeus et al., SoK: MIAs on LLMs are Rushing Nowhere | 2024 | SaTML 2025 | [2406.17975](https://arxiv.org/abs/2406.17975) | ○ | ● | ● | | | |
| 16 | maini2024-dataset-inference | Maini et al., LLM Dataset Inference | 2024 | arXiv ⚠ | [2406.06443](https://arxiv.org/abs/2406.06443) | ○ | ● | | | non | |
| 17 | tong2026-pretraining-data-exposure | Tong et al., Pretraining Data Exposure in LLMs (survey) | 2026 | NLDB 2025 ⚠ | [2605.26133](https://arxiv.org/abs/2605.26133) | ○ | | ● | | | |
| 18 | duan2024-do-mias-work | Duan et al., Do MIAs Work on LLMs? (MIMIR) | 2024 | COLM 2024 | [2402.07841](https://arxiv.org/abs/2402.07841) | ○ | ● | ● | | non | oui |
| 19 | das2024-blind-baselines | Das et al., Blind Baselines Beat MIAs | 2024 | Workshops DATA-FM@ICLR 2025, DLSP 2025 | [2406.16201](https://arxiv.org/abs/2406.16201) | | ● | ○ | | | |
| 20 | zhang2025-mia-cannot-prove | Zhang et al., MIAs Cannot Prove a Model Was Trained On Your Data | 2024 | SaTML 2025 (position) | [2409.19798](https://arxiv.org/abs/2409.19798) | ○ | ● | | | | |
| 21 | hayes2025-limits-strong-mia | Hayes et al., Limits of strong MIAs on LLMs | 2025 | NeurIPS 2025 | [2505.18773](https://arxiv.org/abs/2505.18773) | | ● | | | non | |
| 22 | wang2026-checkmiabench | Wang et al., CheckMIABench | 2026 | ACL 2026 (short) | [ACL](https://aclanthology.org/2026.acl-short.30/), [2606.17464](https://arxiv.org/abs/2606.17464) | | ● | ○ | | non | |
| 23 | shi2026-olmo-detect | Shi et al., OLMo-Detect | 2026 | arXiv | [2610.02986](https://arxiv.org/abs/2610.02986) | | ● | ● | | non | |
| 24 | kim2026-em-mia | Kim et al., EM-MIA (OLMoMIA) | 2024 | EACL 2026 | [2410.07582](https://arxiv.org/abs/2410.07582) | | ● | ● | | non | |
| 25 | puerto2025-scaling-up-mia | Puerto et al., Scaling Up Membership Inference | 2024 | Findings NAACL 2025 | [2411.00154](https://arxiv.org/abs/2411.00154) | | ● | ● | | non | |
| 26 | zhang2025-fsd | Zhang et al., Fine-tuning can Help Detect Pretraining Data (FSD) | 2024 | ICLR 2025 ⚠ | [2410.10880](https://arxiv.org/abs/2410.10880) | | ● | ○ | | non | |
| 27 | zhang2024-dcpdd | Zhang et al., DC-PDD (PatentMIA) | 2024 | EMNLP 2024 | [2409.14781](https://arxiv.org/abs/2409.14781) | | ○ | ● | | partiel | |
| 28 | xie2024-recall | Xie et al., ReCaLL | 2024 | EMNLP 2024 | [2406.15968](https://arxiv.org/abs/2406.15968) | | ○ | | | non | |
| 29 | li2025-ai-coders-snitches | Li et al., Are AI Coders Snitches? (CodeSnitch) | 2025 | arXiv | [2507.17389](https://arxiv.org/abs/2507.17389) | | ● | ○ | oui | non | |
| 30 | li2026-synprune | Li et al., Syntax-Aware Attribution (SynPrune) | 2025 | AAAI 2026 ⚠ | [2511.07033](https://arxiv.org/abs/2511.07033) | | ● | ● | oui | non | |
| 31 | koohestani2026-ast-pac | Koohestani et al., AST-PAC | 2026 | arXiv | [2602.13240](https://arxiv.org/abs/2602.13240) | | ● | ○ | oui | non | |
| 32 | yang2024-gotcha | Yang et al., Gotcha! This Model Uses My Code! | 2023 | IEEE TSE | [2310.01166](https://arxiv.org/abs/2310.01166) | | ● | ● | oui | partiel | |
| 33 | majdinasab2024-trawic | Majdinasab et al., Trained Without My Consent (TraWiC) | 2024 | ACM TOSEM | [2402.09299](https://arxiv.org/abs/2402.09299) | | ● | ● | oui | oui | |
| 34 | riddell2024-code-contamination | Riddell et al., Quantifying Contamination in Code Generation | 2024 | ACL 2024 (long) | [ACL](https://aclanthology.org/2024.acl-long.761), [2403.04811](https://arxiv.org/abs/2403.04811) | | ○ | ● | oui | | |
| 35 | dong2024-cdd | Dong et al., Generalization or Memorization (CDD) | 2024 | ACL 2024 | [2402.15938](https://arxiv.org/abs/2402.15938) | | ● | ● | partiel | oui | |
| 36 | wan2024-code-completion-mia | Wan et al., Does Your Code Completion Model Use My Code? (CodeMI) | 2024 | arXiv | [2404.14296](https://arxiv.org/abs/2404.14296) | ○ | ● | ● | oui | partiel | oui |
| 37 | jiang2025-advprompt-mia-code | Jiang et al., AdvPrompt-MIA | 2025 | arXiv ⚠ | [2511.15107](https://arxiv.org/abs/2511.15107) | | ● | ● | oui | oui | oui |
| 38 | alkaswan2024-memorisation-code | Al-Kaswan et al., Traces of Memorisation in LLMs for Code | 2023 | ICSE 2024 | [2312.11658](https://arxiv.org/abs/2312.11658) | | ○ | ● | oui | | oui |
| 39 | hallinan2025-ngram-coverage | Hallinan et al., MIA with Simple N-Gram Coverage | 2025 | COLM 2025 | [2508.09603](https://arxiv.org/abs/2508.09603) | | ● | | | oui | |
| 40 | kaneko2024-samia | Kaneko et al., SaMIA | 2024 | arXiv | [2404.11262](https://arxiv.org/abs/2404.11262) | | ● | ○ | | oui | |
| 41 | he2025-petal | He et al., Label-Only MIA against Pre-trained LLMs (PETAL) | 2025 | USENIX Security 2025 | [2502.18943](https://arxiv.org/abs/2502.18943) | | ● | | | oui | |
| 42 | yi2026-simmia-wild | Yi et Li, Membership Inference on LLMs in the Wild (WikiMIA-25) | 2026 | arXiv | [2601.11314](https://arxiv.org/abs/2601.11314) | | ● | | | oui | |
| 43 | zhou2025-blackbox-dataset-inference | Zhou et al., Blackbox Dataset Inference for LLM | 2025 | arXiv | [2507.03619](https://arxiv.org/abs/2507.03619) | | ● | | | oui | |
| 44 | duarte2024-de-cop | Duarte et al., DE-COP | 2024 | arXiv ⚠ | [2402.09910](https://arxiv.org/abs/2402.09910) | | ● | | | oui | |
| 45 | golchin2024-time-travel | Golchin et Surdeanu, Time Travel in LLMs | 2023 | ICLR 2024 | [2308.08493](https://arxiv.org/abs/2308.08493) | | ○ | ○ | | oui | |
| 46 | shi2024-min-k-prob | Shi et al., Min-K% Prob (WikiMIA, BookMIA) | 2023 | arXiv | [2310.16789](https://arxiv.org/abs/2310.16789) | | ○ | ● | | non | oui |
| 47 | zhang2025-min-k-plus-plus | Zhang et al., Min-K%++ | 2024 | ICLR 2025 | [2404.02936](https://arxiv.org/abs/2404.02936) | | ○ | | | non | oui |
| 48 | mattern2023-neighbourhood | Mattern et al., Neighbourhood Comparison | 2023 | arXiv | [2305.18462](https://arxiv.org/abs/2305.18462) | | ○ | ● | | non | oui |
| 49 | carlini2021-extracting | Carlini et al., Extracting Training Data from LLMs | 2020 | arXiv | [2012.07805](https://arxiv.org/abs/2012.07805) | | ○ | ○ | | | oui |
| 50 | maity2026-code-provenance | **Maity et al. (encadrants)**, Analyzing Code Provenance in LLMs for Programming Education | 2026 | arXiv | [2611.09177](https://arxiv.org/abs/2611.09177) | | ○ | ● | oui | ? | |
| 51 | baggio2026-rag-algorithmic | Baggio et al. (dont Machado, Maity), RAG and Algorithmic Problem-Solving | 2026 | arXiv | [2611.09791](https://arxiv.org/abs/2611.09791) | | | ○ | oui | | |
| 52 | wu2025-survey-mia-large-models | Wu et Cao, MIAs on Large-Scale Models: A Survey | 2025 | arXiv | [2503.19338](https://arxiv.org/abs/2503.19338) | | | ● | | | |
| 53 | fu2025-contamination-assumptions | Fu et al., Does Data Contamination Detection Work (Well)? | 2025 | Findings NAACL 2025 | [ACL](https://aclanthology.org/2025.findings-naacl.291/) | | ○ | ● | | | |
| 54 | satvaty2024-undesirable-memorization | Satvaty et al., Undesirable Memorization in LLMs: A Survey | 2024 | arXiv | [2410.02650](https://arxiv.org/abs/2410.02650) | | | ● | | | |
| 55 | ravaut2024-contamination-survey | Ravaut et al., Survey of Contamination Detection Methods | 2024 | TMLR 2025 | [2404.00699](https://arxiv.org/abs/2404.00699) | | | ● | | | |
| 56 | xu2024-bdc-survey | Xu et al., Benchmark Data Contamination of LLMs: A Survey | 2024 | arXiv | [2406.04244](https://arxiv.org/abs/2406.04244) | | | ○ | | | |
| 57 | carlini2022-quantifying-memorization | Carlini et al., Quantifying Memorization Across Neural LMs | 2022 | arXiv ⚠ | [2202.07646](https://arxiv.org/abs/2202.07646) | | | ● | | | |
| 58 | kandpal2022-dedup-privacy | Kandpal et al., Deduplicating Training Data Mitigates Privacy Risks | 2022 | ICML 2022 | [2202.06539](https://arxiv.org/abs/2202.06539) | | | ● | | | |
| 59 | biderman2023-emergent-memorization | Biderman et al., Emergent and Predictable Memorization | 2023 | arXiv ⚠ | [2304.11158](https://arxiv.org/abs/2304.11158) | | | ○ | | | |
| 60 | yang2024-unveiling-memorization-code | Yang et al., Unveiling Memorization in Code Models | 2023 | ICSE 2024 | [2308.09932](https://arxiv.org/abs/2308.09932) | | | ● | oui | | |
| 61 | pappu2024-memorization-rlhf-code | Pappu et al., Measuring memorization in RLHF for code completion | 2024 | arXiv | [2406.11715](https://arxiv.org/abs/2406.11715) | | | ○ | oui | | |
| 62 | niu2023-codexleaks | Niu et al., CodexLeaks | 2023 | USENIX Security 2023 | [USENIX](https://www.usenix.org/conference/usenixsecurity23/presentation/niu) | | | ○ | oui | oui | |
| 63 | yang2025-equivalent-transformations-mia | Yang et al., Semantically Equivalent Code Transformations and MIA | 2025 | arXiv ⚠ | [2512.15468](https://arxiv.org/abs/2512.15468) | | ○ | ● | oui | | |
| 64 | yang2023-rephrased-samples | Yang et al., Rethinking Benchmark and Contamination with Rephrased Samples | 2023 | arXiv | [2311.04850](https://arxiv.org/abs/2311.04850) | | | ○ | partiel | | |
| 65 | matton2024-leakage-code-eval | Matton et al., On Leakage of Code Generation Evaluation Datasets | 2024 | Findings EMNLP 2024 | [2407.07565](https://arxiv.org/abs/2407.07565) | | | ○ | oui | | |
| 66 | zhou2025-lessleak-bench | Zhou et al., LessLeak-Bench | 2025 | arXiv | [2502.06215](https://arxiv.org/abs/2502.06215) | | | ○ | oui | | |
| 67 | jain2024-livecodebench | Jain et al., LiveCodeBench | 2024 | arXiv | [2403.07974](https://arxiv.org/abs/2403.07974) | | | ○ | oui | | |
| 68 | oren2023-proving-contamination | Oren et al., Proving Test Set Contamination in Black Box LMs | 2023 | arXiv | [2310.17623](https://arxiv.org/abs/2310.17623) | | | ○ | | partiel | |
| 69 | chauvin2026-logprob-tracking | Chauvin et al., Log Probability Tracking of LLM APIs | 2025 | ICLR 2026 | [2512.03816](https://arxiv.org/abs/2512.03816) | | | ○ | | partiel | |
| 70 | gao2025-model-equality-testing | Gao et al., Model Equality Testing | 2024 | ICLR 2025 | [2410.20247](https://arxiv.org/abs/2410.20247) | | | ○ | | oui | |

Répartition (● ou ○) : Q1 = 20 sources, Q2 = 38, Q3 = 46 (une source peut servir plusieurs questions).

## Q1. Watermarking de code et détection de données d'entraînement

Ce que chaque source éclaire (sans conclure sur la question).

**Watermarking de données de code, côté auteur ou propriétaire**
- **sun2022-coprotector** : le cas fondateur. Des dépôts sont empoisonnés par des watermarks-backdoors, ce qui suppose d'agir sur le code avant sa publication.
- **sun2023-codemark** : des watermarks créés par des transformations qui préservent la sémantique, la même famille d'opérations que les perturbations de CodeTrace.
- **xiao2025-decoma** : une attaque qui détecte et purifie ces watermarks. Elle éclaire la robustesse du marquage face à un entraîneur adverse.
- **chen2026-ducodemark** : l'état récent de cette lignée, avec une réponse aux attaques de purification.
- **qu2025-repomark** : des variantes sémantiquement équivalentes insérées comme marques, puis un test statistique sur le comportement du modèle. C'est la frontière la plus proche entre marquage et comparaison authentique contre perturbé.

**Marquage préalable pour LLM (texte), détecté par des scores de type MIA**
- **meeus2024-copyright-traps** : des pièges insérés par l'auteur, puis détectés avec des scores MIA. Le lien entre les deux familles y est direct.
- **wei2024-data-watermarks** : la « membership » est prouvée par un test d'hypothèse au taux de faux positifs contrôlé. L'abstract mentionne les hash SHA comme watermarks naturels, ce qui fait un pont vers le code.
- **rastogi2025-stamp** : une version publiée et des variantes gardées privées, une structure proche de « authentique contre perturbé ».
- **li2025-provenance-unicode** : un marquage invisible pour auditer le fine-tuning en boîte noire.
- **weinberg2026-sigil** : des canaris dans du texte et du code, détectés par un « membership inference score ». C'est un preprint à auteur unique, évalué en simulation : à prendre avec prudence.

**Taxonomies et articulation avec les MIA**
- **du2025-sok-copyright-auditing** : la taxonomie qui oppose méthodes intrusives (watermarks) et non intrusives (inférence). C'est la plus utile pour situer le watermarking par rapport aux MIA.
- **liu2026-implicit-identity** : un survey qui sépare le watermarking des datasets de celui des sorties, utile pour délimiter le périmètre.
- **tong2026-pretraining-data-exposure** : un survey MIA et contamination. Il sert de point de contrôle sur les frontières habituelles du domaine (l'abstract ne mentionne pas le watermarking).
- **meeus2025-sok-rushing-nowhere** : l'injection préalable de séquences y sert de protocole d'évaluation des MIA. C'est un autre rôle possible du marquage.
- **maini2024-dataset-inference** et **zhang2025-mia-cannot-prove** : l'alternative sans marquage pour le propriétaire de données, et l'argument selon lequel les canaris seraient nécessaires comme preuve.
- **wan2024-code-completion-mia** (papers/) : l'approche non intrusive côté code, à mettre en regard.

**Hors périmètre, à distinguer** (watermarking des sorties d'un LLM, relié à la provenance)
- **sander2024-radioactive** : le marquage est fait par le fournisseur du LLM source, pas par l'auteur des données.
- **jovanovic2025-ward** : il compare watermark et MIA, mais pour le RAG, pas pour l'entraînement.

## Q2. Les MIA sur LLM font-elles à peine mieux que le hasard en évaluation propre ? Réponses depuis

**Les deux papiers de départ**
- **duan2024-do-mias-work** (papers/) : MIMIR, modèles entraînés sur le Pile, rôle des décalages de distribution.
- **das2024-blind-baselines** : référence de « Das et al. 2024 » confirmée. Il propose des baselines qui n'interrogent pas le modèle, à reproduire (et CLAUDE.md impose déjà une baseline temporelle).

**Diagnostics convergents et critiques conceptuelles**
- **meeus2025-sok-rushing-nowhere** : une critique indépendante, avec des recommandations de protocole (splits aléatoires, injection, contrôles post hoc).
- **maini2024-dataset-inference** : un diagnostic du même problème, et une réponse qui passe au niveau du dataset.
- **zhang2025-mia-cannot-prove** : une critique de l'usage des MIA comme preuve, qui touche l'objectif d'audit de CodeTrace.
- **hayes2025-limits-strong-mia** : des attaques fortes (LiRA avec modèles de référence) dans un cadre contrôlé. Il sépare la faiblesse due à la conception de l'attaque d'une limite de fond.

**Benchmarks construits pour éviter le biais**
- **wang2026-checkmiabench** : membres et non-membres de même distribution, tirés des checkpoints de Pythia et d'OLMo.
- **shi2026-olmo-detect** : contrôle des facteurs confondants, plusieurs phases d'entraînement, variante avec et sans décalage.
- **kim2026-em-mia** : le benchmark OLMoMIA, où la séparabilité varie, et la méthode EM-MIA.
- **puerto2025-scaling-up-mia** : agrégation de la phrase à la collection. Pertinent si CodeTrace teste un dépôt entier.

**Nouvelles méthodes, à examiner selon le benchmark utilisé**
- **zhang2025-fsd** (recalibration par fine-tuning), **zhang2024-dcpdd** (calibration par fréquence, PatentMIA) et **xie2024-recall** (évalué surtout sur WikiMIA) : il faut vérifier dans les PDF sur quels splits les gains sont mesurés.
- Contexte déjà dans papers/ : **shi2024-min-k-prob** (WikiMIA, cible directe des critiques), **zhang2025-min-k-plus-plus**, **mattern2023-neighbourhood**, **carlini2021-extracting**.

**Code**
- **li2025-ai-coders-snitches** : l'étude empirique la plus directe sur le code (7 méthodes, 8 modèles de code), avec des mutations par type de clone proches des perturbations de CodeTrace.
- **li2026-synprune** : un score qui exclut les tokens imposés par la syntaxe. Le split est possiblement temporel, à vérifier.
- **koohestani2026-ast-pac** : des perturbations guidées par l'AST, au plus près de l'idée « authentique contre perturbé » sur du code.
- **yang2024-gotcha** et **wan2024-code-completion-mia** (papers/) : MIA sur du code antérieures aux critiques, avec des protocoles à modèles substituts à réexaminer.
- **majdinasab2024-trawic** : une détection fondée sur les complétions d'identifiants, candidate pour les API sans logprobs du prompt.
- **jiang2025-advprompt-mia-code** (papers/) : des prompts adverses, revendiqués comme boîte noire.
- **riddell2024-code-contamination** et **dong2024-cdd** : une vérité terrain par recherche dans le corpus, et une détection sur sorties échantillonnées (HumanEval).
- **alkaswan2024-memorisation-code** (papers/) : contexte sur la mémorisation du code.

**Boîte noire en général**
- **hallinan2025-ngram-coverage**, **kaneko2024-samia** et **yi2026-simmia-wild** : des scores calculés sur le texte généré seul. Hallinan teste des modèles OpenAI. WikiMIA-25 est construit de façon temporelle, donc il faut vérifier comment le biais est contrôlé.
- **he2025-petal** : du label-only strict. L'abstract discute les attaques fondées sur la robustesse aux perturbations, ce qui concerne directement l'hypothèse de CodeTrace.
- **zhou2025-blackbox-dataset-inference** : l'inférence au niveau du dataset avec les seules réponses textuelles.
- **duarte2024-de-cop** : un QCM entre l'original et ses paraphrases, analogue à « authentique contre perturbé ».
- **golchin2024-time-travel** : une complétion guidée sur API fermée.

## Q3. Constats solides et zones ouvertes

**Papiers de l'équipe encadrante (à lire en priorité)**
- **maity2026-code-provenance** : extension de Min-K% avec génération synthétique de non-membres, sur du code Python. Il évalue GPT-5, Gemini 2.5, Mistral, DeepSeek et LLaMA 3.3, soit les modèles du sujet CodeTrace. L'abstract ne dit pas comment les logprobs des modèles commerciaux sont obtenus.
- **baggio2026-rag-algorithmic** : une analyse Min-K sert de contrôle de mémorisation dans une évaluation de génération de code.

**Surveys et SoK avec une section sur les problèmes ouverts**
- **wu2025-survey-mia-large-models** et **tong2026-pretraining-data-exposure** : une section défis ouverts est annoncée dans l'abstract.
- **xu2024-bdc-survey** : une section challenges and future directions est annoncée.
- **fu2025-contamination-assumptions** : confronte les hypothèses implicites des méthodes à leur validité empirique, pour séparer ce qui est établi de ce qui est ouvert.
- **satvaty2024-undesirable-memorization** et **ravaut2024-contamination-survey** : les taxonomies de la mémorisation et des méthodes de détection.
- **meeus2025-sok-rushing-nowhere** : la SoK de référence sur les protocoles d'évaluation.

**Benchmarks de référence**
- WikiMIA et BookMIA (**shi2024-min-k-prob**), MIMIR (**duan2024-do-mias-work**), PatentMIA (**zhang2024-dcpdd**), OLMoMIA (**kim2026-em-mia**), **shi2026-olmo-detect** et **puerto2025-scaling-up-mia**.

**Facteurs de mémorisation et de détectabilité**
- **carlini2022-quantifying-memorization** : la taille du modèle, la duplication et la longueur du contexte.
- **kandpal2022-dedup-privacy** : la duplication et la déduplication, à rapprocher de The Stack, qui est dédupliqué.
- **biderman2023-emergent-memorization** : jusqu'où la mémorisation est prévisible.
- **zhang2025-fsd** et **pappu2024-memorization-rlhf-code** : l'effet du fine-tuning et du RLHF, ce qui compte pour les modèles instruct visés.

**Mémorisation et MIA sur du code**
- **yang2024-unveiling-memorization-code**, **alkaswan2024-memorisation-code** (papers/), **yang2024-gotcha**, **majdinasab2024-trawic**, **li2026-synprune**, **wan2024-code-completion-mia** (papers/) et **niu2023-codexleaks** (un modèle de code fermé, Copilot).

**Perturbations de code**
- **yang2025-equivalent-transformations-mia** : la seule étude systématique trouvée sur les transformations équivalentes et les MIA de code. Elle prend l'angle de l'évasion, ce qui en fait le contrepoint direct de l'hypothèse de CodeTrace.
- **jiang2025-advprompt-mia-code** et **mattern2023-neighbourhood** (papers/) : les deux références centrales de cet axe.

**Contamination des benchmarks de code**
- **riddell2024-code-contamination**, **yang2023-rephrased-samples**, **matton2024-leakage-code-eval**, **zhou2025-lessleak-bench**, **dong2024-cdd**.
- **jain2024-livecodebench** : une source de non-membres datés, à croiser avec le biais temporel.
- **oren2023-proving-contamination** et **golchin2024-time-travel** : un test statistique au niveau du dataset, et une méthode par génération.

**Audit de modèles servis par API**
- **chauvin2026-logprob-tracking** : le non-déterminisme des logprobs d'API et leur usage statistique.
- **gao2025-model-equality-testing** : un provider peut ne pas servir exactement les poids annoncés, ce qui pèse sur la reproductibilité.
- **kaneko2024-samia** : une MIA sans logprobs.

## Points à vérifier avant de citer

- **Venues non confirmées (⚠)** :
  - **maini2024-dataset-inference** et **duarte2024-de-cop** : aucun venue sur arXiv (les sous-agents évoquent NeurIPS 2024 et ICML 2024, de mémoire).
  - **carlini2022-quantifying-memorization** et **biderman2023-emergent-memorization** : aucun venue sur arXiv (ICLR 2023 et NeurIPS 2023 de mémoire).
  - **zhang2025-fsd** : ICLR 2025 selon proceedings.iclr.cc, d'après un sous-agent. Le champ arXiv est vide.
  - **li2026-synprune** : AAAI 2026 selon le commentaire arXiv, mais pas vu dans les actes.
  - **jiang2025-advprompt-mia-code** : ASE 2025 selon un résultat de recherche seulement.
  - **yang2025-equivalent-transformations-mia** : ICSE 2026 selon conf.researchr.org, page non ouverte.
  - **tong2026-pretraining-data-exposure** : déposé sur arXiv en mai 2026 mais annoncé « accepted by NLDB 2025 ».
  - OpenReview a bloqué l'accès automatisé, d'où ces trous.
- **Titres qui ont changé depuis la v1** : **hayes2025-limits-strong-mia** et **li2025-ai-coders-snitches**. Il faut citer les titres de ce tableau.
- **Splits membres et non-membres sur le code** : aucun abstract ne décrit comment ils sont construits (CodeSnitch, SynPrune, AST-PAC, CodeMI). Il faut le lire dans les PDF, à cause du biais temporel.
- **Papier de Maity et al. sur l'audit d'API via les token probabilities** : introuvable sous cette forme. La recherche a couvert l'API arXiv (auteur Maity Subhankar) et le web, mais dblp était bloqué. Le plus proche est **maity2026-code-provenance**. Il faut demander la référence exacte aux encadrants.

## Pistes non confirmées (non retenues dans le tableau)

- SrcMarker (arXiv 2309.00860) : watermarking de code source, peut-être orienté vers l'auteur plutôt que vers l'entraînement.
- arXiv 2411.05051 : survey sur la protection de la propriété intellectuelle des modèles et des datasets.
- arXiv 2508.11548 : survey sur la protection du copyright des LLM.
- arXiv 2606.23030 : MIA label-only au niveau entité.
- arXiv 2405.11430 (MHPP) : contamination de MBPP et HumanEval.
- « A Missing Testbed for LLM Pre-Training Membership Inference Attacks » (ICLR 2025) : auteurs non vérifiés.
- Yang et al. (arXiv 2403.07506) : revue systématique sur les LLM de code, pertinence faible.
- Recherches restées sans résultat : aucun benchmark MIA de code largement adopté (un équivalent de WikiMIA pour le code), aucun « copyright trap » propre au code, aucune « critique des critiques » explicite qui défendrait les anciens benchmarks.

## Requêtes effectuées (résumé)

- Q1 : watermarking de datasets de code (CoProtector, CodeMark, DeCoMa), data watermarks et canaris pour LLM, SoK sur l'audit de copyright des datasets, surveys watermarking et fingerprinting, Ward.
- Q2 : Duan et Das, décalage de distribution dans WikiMIA et MIMIR, benchmarks IID sur OLMo et Pythia, FSD, label-only et n-gram coverage en boîte noire, détection de données d'entraînement sur des LLM de code (StarCoder, The Stack), contamination de code (Riddell).
- Q3 : surveys MIA, contamination et mémorisation avec problèmes ouverts, transformations sémantiquement équivalentes et MIA de code, SynPrune, contamination HumanEval et MBPP, API arXiv `au:Maity_Subhankar`.
- Recontrôle final : API arXiv `id_list` (68 identifiants), BibTeX ACL Anthology (3), page USENIX (1).
