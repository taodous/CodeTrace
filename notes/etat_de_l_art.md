# État de l'art : provenance des données d'entraînement des LLM pour le code

*Version courte, rédigée le 2026-11-12. Sources : les 8 PDF de `papers/` (résumés lus, pas encore de fiches détaillées) et une recherche web. Les chiffres marqués (web) n'ont été lus que dans des résumés en ligne : il faut les vérifier dans les papiers avant de les citer dans le rapport.*

## 1. Le problème

La question de CodeTrace est un cas de **membership inference attack (MIA)** : étant donné un extrait `x` et un modèle `M`, décider si `x` faisait partie des données d'entraînement de `M`. Pour les LLM, on parle aussi de **pretraining data detection**. Il existe trois niveaux de granularité :

- **niveau échantillon** (un extrait de code donné) : c'est le cadre classique des MIA ;
- **niveau jeu de données** (un dépôt ou un ensemble de fichiers) : c'est la *dataset inference* ;
- **traçage actif** : on marque son code *avant* sa publication (watermarking) pour pouvoir prouver plus tard qu'il a servi à l'entraînement.

Les motivations sont la propriété intellectuelle (licences GPL, CC-BY-SA), les fuites de secrets (clés API, identifiants), la contamination des benchmarks et, comme le souligne le sujet, l'évaluation pédagogique.

## 2. Fondations : MIA sur les LLM en langage naturel

| Famille | Idée | Référence |
|---|---|---|
| Loss / perplexité, ratio zlib | Un membre a une perte plus faible. On normalise par la compressibilité zlib pour corriger la difficulté intrinsèque du texte. | Carlini et al. 2021 (`papers/`) |
| Modèle de référence | On compare la perte du modèle cible à celle d'un modèle de référence entraîné sur des données similaires. C'est efficace, mais coûteux et souvent irréaliste. | cité par Mattern et al. |
| **Comparaison avec des voisins** | On génère des voisins perturbés de `x` (remplacement de mots) et on compare la perte sur `x` à la perte moyenne sur les voisins. Cela remplace le modèle de référence. **C'est l'idée la plus proche de CodeTrace.** | Mattern et al. 2023 (`papers/`) |
| Min-K% Prob | Un texte non vu contient quelques tokens « aberrants » de faible probabilité. On fait la moyenne des k% plus faibles log-probas. Le papier introduit aussi le benchmark WikiMIA (split temporel). | Shi et al. 2024 (`papers/`) |
| Min-K%++ | Les échantillons d'entraînement tendent à être des maxima locaux de la distribution. On normalise la log-proba de chaque token par la moyenne et l'écart-type de la distribution conditionnelle sur le vocabulaire. Cette méthode est l'état de l'art sans référence sur WikiMIA et MIMIR. | Zhang et al. 2025 (`papers/`) |

Ce que ces méthodes demandent : **les log-probabilités des tokens de l'entrée**, et même la distribution complète sur le vocabulaire pour Min-K%++.

## 3. La remise en question méthodologique (2024-2026)

C'est le point le plus important de la littérature récente, et il conditionne directement le protocole de CodeTrace.

- **Duan et al. 2024** (`papers/`, benchmark MIMIR sur Pythia et la Pile) : sur des membres et non-membres tirés de la *même* distribution, les MIA font à peine mieux que le hasard. Il y a deux causes : un corpus énorme vu peu de fois, et une frontière floue entre membres et non-membres. Les succès rapportés ailleurs s'expliquent souvent par un **décalage temporel** entre les deux classes. Les MIA sont aussi très sensibles à de petites modifications de l'échantillon.
- **Das, Zhang et Tramèr 2024, « Blind Baselines »** (web, arXiv 2406.16201) : des classifieurs qui **n'interrogent pas du tout le modèle** battent les meilleures MIA publiées sur 8 jeux d'évaluation. La conclusion est que presque tous les benchmarks MIA pour les foundation models sont biaisés.
- **Maini et al. 2024, « LLM Dataset Inference »** (web, NeurIPS 2024, arXiv 2406.06443) : ils proposent de passer du niveau échantillon au **niveau jeu de données**. On agrège plusieurs scores MIA puis on fait un test statistique sur un ensemble suspect, environ 1000 séquences d'après le résumé. Ce cadre colle bien au cas d'usage « mon dépôt a-t-il été utilisé ? ».
- **SoK « MIAs on LLMs are rushing nowhere »** (web, arXiv 2406.17975) : synthèse qui va dans le même sens et propose des pistes de correction (splits aléatoires contrôlés, données à cutoff certain).

**Conséquence pour CodeTrace :** une baseline aveugle (un classifieur « code ancien contre code récent » sans le modèle) est obligatoire, comme le prévoit déjà `CLAUDE.md`. Les labels doivent venir d'un corpus d'entraînement connu (The Stack, la Pile, OLMo) plutôt que de la seule date.

## 4. Travaux spécifiques au code

| Travail | Accès | Apport |
|---|---|---|
| Al-Kaswan et al. 2024 (`papers/`) | Génération | Les LLM de code sont vulnérables à l'extraction : 47 % des échantillons jugés extractibles ont été extraits de CodeGen-Mono-16B. La mémorisation augmente avec la taille du modèle, et les « data carriers » (fichiers de données, constantes) sont plus mémorisés que le code ordinaire. |
| Wan et al. 2024, CodeMI (`papers/`) | Boîte noire + shadow models | Adapte les MIA à la complétion de code avec des modèles fantômes. L'attaque marche sur LSTM et CodeGPT (accuracy 0,842 et 0,730), mais **l'appartenance est difficile à détecter sur CodeGen et StarCoder**. |
| Yang et al., GotCha (web, arXiv 2310.01166) | Gris + modèle substitut | MIA pour les modèles de code. Elle sert de baseline aux travaux suivants. |
| Zhang & Li (web, arXiv 2312.07200) | Boîte noire | Détecter l'usage non autorisé de code dans les modèles pré-entraînés de code. |
| **Jiang et al. 2025, AdvPrompt-MIA** (`papers/`) | Boîte noire, complétions | On génère des **perturbations de code qui préservent la sémantique** (prompts adverses), on compare les complétions à la vérité terrain, puis on entraîne un classifieur sur ces vecteurs de features. Les auteurs annoncent jusqu'à +102 % d'AUC par rapport aux baselines. **C'est le plus proche du « authentique vs perturbé » de CodeTrace**, mais la méthode reste centrée sur des modèles de complétion. |
| SynPrune (web, arXiv 2511.07033, AAAI 2026) | Log-probas | Avant le scoring, on retire les tokens **imposés par la syntaxe Python** (47 conventions tirées de la référence du langage), car ils sont prévisibles pour tout modèle et brouillent le signal. Le papier fournit un benchmark Python avec des membres issus de la Pile et des non-membres postérieurs au cutoff. |
| Transformations sémantiquement équivalentes (web, arXiv 2512.15468) | Log-probas | Étudie l'effet du renommage, du reformatage, etc. sur les MIA. Le renommage de variables ferait baisser le succès d'environ 10 % (web, à vérifier). Cela montre que la perturbation est à la fois **un outil de détection et un moyen d'évasion**. |

**Ce qui distingue le code du langage naturel :** une grande part des tokens est déterminée par la syntaxe, d'où l'idée de SynPrune. Le code est très dupliqué (forks, boilerplate, licences), ce qui rend la frontière entre membre et non-membre encore plus floue. Enfin, il existe des transformations qui préservent exactement la sémantique (renommage, reformatage, réordonnancement, commentaires). Ces transformations sont un levier naturel pour fabriquer des « voisins » à la Mattern sans recourir à un modèle de langue.

## 5. Accès boîte noire : le verrou des API fermées

Les scores des sections 2 et 4 supposent l'accès aux log-probas **du code fourni en entrée**. Les API commerciales (OpenAI, Gemini) ne semblent exposer que les log-probas des tokens *générés*, et en nombre limité (top-k). C'est à confirmer dans `docs/model_access.md`. Plusieurs travaux récents ciblent ce cadre où l'on n'observe que du texte :

- **N-Gram Coverage Attack** (web, arXiv 2508.09603) : on donne un préfixe, on échantillonne des continuations et on mesure leur recouvrement en n-grammes avec le vrai suffixe. La méthode n'utilise que du texte. Les auteurs observent que les modèles récents (GPT-4o) sont plus robustes.
- **SimMIA** (web, arXiv 2601.11314) : estime le comportement local du modèle à partir du seul mot suivant échantillonné, avec un nouveau benchmark WikiMIA-25 pour modèles fermés.
- **PETAL** (web, arXiv 2502.18943) : attaque *label-only* fondée sur la similarité sémantique des tokens générés.
- Côté audit d'API, **Log Probability Tracking of LLM APIs** (Chauvin et al., ICLR 2026, arXiv 2512.03816) utilise les logprobs pour détecter des changements de modèle derrière une API. L'article des encadrants (Maity et al., ICWS 2026, *Auditing Black-Box LLM APIs via Token Probabilities and Data Provenance: A Case Study in Source Code Generation*) se situe à ce croisement, mais nous ne l'avons pas trouvé en ligne. Il faut le demander aux encadrants.

Pour CodeTrace, cela suggère deux protocoles. Avec les modèles open-weights (Mistral, LLaMA, DeepSeek), on peut utiliser les scores sur les log-probas du prompt. Avec GPT-5 et Gemini, il faut des scores fondés sur la **complétion** : on donne un préfixe du code authentique ou perturbé, puis on mesure la fidélité de la suite générée.

## 6. Approche proactive : le watermarking de code

Au lieu d'inférer l'appartenance après coup, on peut marquer le code avant sa publication :

- **CoProtector** (Sun et al. 2022) : insertion de code mort servant de marque ;
- **CodeMark** (Sun et al. 2023, arXiv 2308.14401) : marques imperceptibles obtenues par transformations qui préservent la sémantique ;
- **TraWiC** : détection de l'inclusion de code dans l'entraînement, présentée comme agnostique au modèle et interprétable.

Ces méthodes ont des limites. L'efficacité de CoProtector et CodeMark est remise en cause par des travaux ultérieurs, et des attaques comme **DeCoMa** détectent et purgent ces marques (web). Surtout, elles ne s'appliquent pas au code déjà publié, qui est justement la cible de CodeTrace.

## 7. Synthèse et positionnement de CodeTrace

1. **Consensus :** les MIA par échantillon sur de gros LLM pré-entraînés donnent un signal faible quand l'évaluation est propre. Beaucoup de résultats positifs s'expliquent par un biais de distribution.
2. **Tendance :** on passe au niveau jeu de données (tests statistiques agrégés), on développe des méthodes sans logprobs pour les API fermées, et on adapte les méthodes à la structure du code (syntaxe, transformations sémantiques).
3. **Lacune que CodeTrace peut combler :**
   - comparer *systématiquement* le comportement sur le code authentique et sur des variantes sémantiquement équivalentes, sur des LLM généralistes récents, ouverts **et** fermés, et pas seulement sur des modèles de complétion ;
   - utiliser des labels fiables (corpus connus) et des baselines aveugles ;
   - analyser l'effet du type de code (langage, boilerplate, data carriers) et de l'architecture du modèle ;
   - proposer un outil interactif, ce qui est peu présent dans la littérature.

## Références

**Dans `papers/` :**
- Carlini et al. 2021, *Extracting Training Data from Large Language Models*, arXiv 2012.07805
- Mattern et al. 2023, *MIA against Language Models via Neighbourhood Comparison*, arXiv 2305.18462
- Shi et al. 2024, *Detecting Pretraining Data from LLMs* (Min-K%), ICLR 2024, arXiv 2310.16789
- Zhang et al. 2025, *Min-K%++*, ICLR 2025, arXiv 2404.02936
- Duan et al. 2024, *Do MIAs Work on LLMs?*, arXiv 2402.07841
- Wan et al. 2024, *Does Your Neural Code Completion Model Use My Code?*, arXiv 2404.14296
- Al-Kaswan et al. 2024, *Traces of Memorisation in LLMs for Code*, arXiv 2312.11658
- Jiang et al. 2025, *Code MIA via Adversarial Prompts*, arXiv 2511.15107

**Trouvées sur le web (pas encore dans `papers/`) :**
- [Das, Zhang, Tramèr 2024, Blind Baselines Beat MIAs for Foundation Models](https://arxiv.org/abs/2406.16201)
- [Maini et al. 2024, LLM Dataset Inference](https://arxiv.org/abs/2406.06443)
- [SoK: MIAs on LLMs are Rushing Nowhere](https://arxiv.org/abs/2406.17975)
- [SynPrune: Uncovering Pretraining Code in LLMs](https://arxiv.org/abs/2511.07033)
- [How Do Semantically Equivalent Code Transformations Impact MIA on LLMs for Code?](https://arxiv.org/abs/2512.15468)
- [Code Membership Inference for Detecting Unauthorized Data Use](https://arxiv.org/abs/2312.07200)
- [GotCha (Yang et al.)](https://arxiv.org/abs/2310.01166)
- [N-Gram Coverage Attack](https://arxiv.org/abs/2508.09603)
- [SimMIA: Membership Inference on LLMs in the Wild](https://arxiv.org/abs/2601.11314)
- [PETAL: Label-Only MIA against Pre-trained LLMs](https://arxiv.org/abs/2502.18943)
- [Log Probability Tracking of LLM APIs](https://arxiv.org/abs/2512.03816)
- [EM-MIA / OLMoMIA](https://arxiv.org/abs/2410.07582)
- [CodeMark](https://arxiv.org/abs/2308.14401)
