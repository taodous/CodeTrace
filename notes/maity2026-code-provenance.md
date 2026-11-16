# Fiche : Maity et al. 2026, Analyzing Code Provenance in LLMs for Programming Education

Statut : lue le 2026-11-15. Source de lecture : extraction texte (pdftotext -layout) du PDF
papers/mia-code/maity2026-code-provenance.pdf (le PDF n'est pas chiffré, mais l'outil de lecture du
sous-agent a échoué dessus). Algorithme 1 (p. 5) et Tableau 1 (p. 7) revérifiés ensuite sur le
rendu image des pages, et corrigés ci-dessous. Les autres symboles signalés [symbole illisible]
restent à revérifier sur le PDF avant citation.

Note de contexte : Maity et Machado sont les encadrants de CodeTrace. Les questions ouvertes de
cette fiche peuvent leur être posées directement (voir fin de fiche).

## 1. Référence

```bibtex
@misc{maity2026codeprovenance,
  author        = {Maity, Subhankar and Belbachir, Faiza and Boucelma, Omar and Medeiros Machado, Guilherme},
  title         = {Analyzing Code Provenance in {LLMs} for Programming Education},
  year          = {2026},
  month         = nov,
  eprint        = {2611.09177},
  archivePrefix = {arXiv},
  primaryClass  = {cs.AI},
  note          = {Preprint, soumis le 2026-11-06, aucun venue indiqué}
}
```

Affiliations : LyRIDS, ECE Research Center (Paris) ; Aix Marseille Univ, Université de Toulon,
CNRS, LIS (Boucelma).

## 2. Problème et hypothèse (3 phrases)

Les LLM produisent instantanément du code fonctionnel, ce qui rend les rendus d'étudiants peu
fiables comme indicateurs d'apprentissage ; les auteurs veulent tracer la provenance du code
(Section 1). Ils formulent la provenance comme une MIA binaire : un extrait de code a-t-il été vu
à l'entraînement du modèle (Section 3) ? Hypothèse : les membres reçoivent des probabilités de
tokens plus élevées (perplexité plus faible) que les non-membres, et la moyenne des k plus faibles
log-probabilités (Min-K%, Shi et al. 2024) est plus discriminante que la perplexité moyenne
(Sections 3 et 4).

## 3. Méthode

### Score (Algorithme 1, Section 4)

Pour une séquence de tokens de code $x = x_1, \dots, x_n$ :

$$
\ell_i = \log p_f(x_i \mid x_1, \dots, x_{i-1}), \quad i = 1, \dots, n
$$

$$
L_{\text{sorted}}(x) = \text{tri croissant de } (\ell_1, \dots, \ell_n), \qquad
\text{Min-}k(x) = L_{\text{sorted}}(x)[1:k]
$$

$$
S_{\text{MinK}}(x) = \frac{1}{k} \sum_{i=1}^{k} \text{Min-}k\%(x)[i]
$$

Décision (Algorithme 1, lignes 7 à 11, vérifié sur le rendu de la p. 5) : si
$S_{\text{MinK}}(x) \ge \tau$ alors Non-Member, sinon Member. **Attention** : tel qu'imprimé, c'est
l'inverse de Min-K% (Shi et al.), où un score élevé (log-probabilités peu négatives, texte peu
surprenant) indique un membre. Soit c'est une coquille, soit l'implémentation utilise la
log-probabilité négative ; la Section 4 dit pourtant "Training data typically yield higher token
probabilities". Question à poser aux auteurs.

Ambiguïté sur k : le texte parle des "lowest K%" tokens (Section 4), mais l'Algorithme 1 extrait
"the lowest k log-probabilities" et le setup (Section 5) teste "fixed values of the hyperparameter
k, such as k = 5, 10, 20" décrits comme "number of lowest token probabilities". Il n'est donc pas
clair si k est un nombre absolu de tokens ou un pourcentage de n. Retenu : k = 10 (Section 5).

### Seuil (Section 4, "Threshold Selection")

Suivant [32] (Zanella-Beguelin et al. 2023) :

$$
\tau = \frac{1}{2}\left( Q_{75}(\{S(x) : x \in \text{membres}\}) + Q_{25}(\{S(x) : x \in \text{non-membres}\}) \right)
$$

calculé sur 30 % des données (calibration), évaluation sur les 70 % restants (Section 5).

### Contribution annoncée : non-membres synthétiques (Algorithme 2, Section 5)

Chaque extrait membre $c$ est transformé par une seule stratégie tirée avec $r \sim U(0,1)$ :

| Stratégie | Proba | Description (Section 5) |
|---|---|---|
| Semantic Transformation | 15 % | renommage aléatoire des variables et fonctions, modification, suppression ou paraphrase des commentaires |
| Structural Transformation | 15 % | indentation, espacement, formatage, réordonnancement du flot de contrôle et des blocs |
| Aggressive Transformation | 40 % | injection de logique redondante ou équivalente, et casse volontaire de la logique en gardant la syntaxe valide |
| Cross Language Conversion | 25 % | réécriture dans la syntaxe d'autres langages ou frameworks (JavaScript, Java, C++, GraphQL, notebooks Jupyter) |
| Novel Pattern Generation | 5 % | structures hors Python : SQL/NoSQL, Kubernetes, Docker, Terraform |

Le papier ne dit pas comment ces transformations sont implémentées (règles AST, regex, LLM
générateur ?). Validation : distance d'édition d'arbre AST normalisée [28] entre original et
synthétique sur 500 paires, moyenne 0.996 (Section 5).

### Accès requis

- Section 3 : "black-box setting in which the detector can only query f to obtain token
  probabilities for the input x". Le score exige donc les logprobs des tokens d'ENTRÉE (le code
  fourni), pour chaque position. C'est un accès boîte grise (logprobs du prompt), pas une boîte
  noire au sens "texte généré seulement".
- Modèles gratuits : via Hugging Face (Section 5), donc accès complet aux logits.
- Modèles commerciaux : "using OpenRouter APIs" (Section 5, note 4). **Le papier ne dit pas
  comment les logprobs des tokens d'entrée sont obtenus via OpenRouter** pour GPT-5,
  Gemini-2.5-Flash, Mistral-Small-24B-Instruct, DeepSeek-V3 et LLaMA-3.3-70B-Instruct : ni
  paramètre d'API (echo, prompt_logprobs, top_logprobs), ni provider sous-jacent, ni contournement
  (par exemple scorer une complétion, ou reconstruire les logprobs token par token en générant).
  Question à poser aux auteurs (nos encadrants). Voir aussi rubrique 6.

## 4. Setup expérimental

- **Modèles gratuits** (Section 5, Tableau 2) : DialoGPT-medium, DialoGPT-large, GPT-2,
  DistilGPT-2, via Hugging Face, environ 3000 échantillons par classe. GPU NVIDIA Tesla T4.
- **Modèles payants** (Section 5, Tableau 2) : GPT-5, Gemini-2.5-Flash, Mistral-Small-24B-Instruct,
  DeepSeek-V3, LLaMA-3.3-70B-Instruct, via OpenRouter, environ 200 échantillons par classe "due to
  budget constraints". Choix justifié par l'usage étudiant et un leaderboard code d'octobre 2025.
- **Membres** (Section 5, "Member Data") : champ `answer` des enregistrements Python de ProCQA
  [17] (Li et al., LREC-COLING 2024 ; environ 1.008 M enregistrements Python, issus de Stack
  Overflow). Ils sont *supposés* membres : le papier ne vérifie ni la date de publication des
  réponses, ni les dates de cutoff des modèles, ni la présence dans un corpus d'entraînement connu.
  Le Tableau 1 donne la répartition par concept de programmation (curriculum MIT OCW).
- **Non-membres** : sorties de l'Algorithme 2 appliqué aux membres. Aucun non-membre "naturel"
  (par exemple réponses Stack Overflow postérieures au cutoff).
- **Contrôle du biais de distribution** : aucun. La seule vérification est la distance AST de
  0.996, qui mesure que les synthétiques sont éloignés des originaux, pas qu'ils viennent de la
  même distribution.
- **Split** : 30 % calibration du seuil, 70 % évaluation. Choix de k parmi {5, 10, 20} ; le papier
  ne dit pas sur quel split k a été choisi.
- **Métriques** (Section 5, "Metrics") : AUC, TPR@5%FPR, précision, F1. Pas de TPR@1%FPR.
- **Preuve de concept éducative** (Section 7) : notebooks Jupyter de 5 groupes (7 étudiants par
  groupe) d'un hackathon data science sur Titanic, avec consentement ; vérité terrain = logs de
  conversation LLM partagés par les étudiants. Alignement prédictions / logs par 4 stratégies
  (match exact normalisé, fuzzy caractère, fuzzy token, Jaccard). Non précisé : modèle(s) scorés,
  granularité exacte (le texte parle de "line-level code data"), nombre de segments, calibration du
  seuil sur ces données.

## 5. Résultats clés

Tableau 2 (Stack Overflow / ProCQA, membres vs synthétiques). TPR@5%FPR en %.

| Modèle | Accès | AUC | TPR@5%FPR (%) | Précision | F1 |
|---|---|---|---|---|---|
| DialoGPT-medium | HF | 0.577 | 9.24 | 0.564 | 0.543 |
| DialoGPT-large | HF | 0.585 | 10.28 | 0.608 | 0.471 |
| GPT-2 | HF | 0.664 | **18.19** | 0.651 | 0.631 |
| DistilGPT-2 | HF | **0.713** | 17.24 | **0.680** | **0.674** |
| Gemini-2.5-Flash | OpenRouter | **0.654** | 6.16 | 0.567 | 0.666 |
| Mistral-Small-24B-Instruct | OpenRouter | 0.535 | 7.29 | 0.509 | 0.639 |
| DeepSeek-V3 | OpenRouter | 0.540 | 5.86 | 0.500 | 0.666 |
| LLaMA-3.3-70B-Instruct | OpenRouter | 0.559 | 7.48 | 0.557 | **0.667** |
| GPT-5 | OpenRouter | 0.566 | **10.14** | **0.569** | 0.577 |

Tableau 3 (preuve de concept étudiants) : AUC entre 0.584 (groupe 1) et 0.644 (groupe 4) ;
TPR@5%FPR entre 6.25 et 8.24 % ; précision entre 0.233 (groupe 5) et 0.895 (groupe 2) ; F1 entre
0.368 et 0.780.

Autres affirmations du papier :
- Fig. 2 : pas de corrélation simple entre taille du modèle et AUC (constat visuel, pas de test).
- Section 7 : l'implémentation attribue la plus forte probabilité à GPT-5 (ChatGPT) pour tous les
  groupes, ce que confirment les logs. La méthode d'attribution à un modèle n'est pas décrite.
- Aucun intervalle de confiance, aucun test statistique, aucune seed rapportée.

## 6. Limites et biais possibles

### Ce que le papier reconnaît lui-même
- Moins d'échantillons pour les modèles payants (environ 200 par classe) pour raison de coût
  (Sections 5 et 6).
- La méthode détecte l'appartenance au training set et peut confondre génération par IA et
  récupération manuelle sur le web (Stack Overflow) (Section 8).

### Ecart gratuits / payants : mesuré vs avancé
- **Mesuré** : AUC plus faibles pour les modèles payants (0.535 à 0.654) que pour les gratuits
  (0.577 à 0.713) (Tableau 2).
- **Avancé sans expérience** (Section 6) : l'écart serait "primarily due to intentional design
  choices made by providers aimed at enhancing user privacy" ; mécanismes cités : differential
  privacy, noise injection, architectures orientées sécurité, restrictions d'API, régularisation et
  exposition sélective des données, tous appuyés sur un survey [31] et non testés sur ces modèles.
  Le papier mentionne aussi les différences de calcul et d'agrégation des token probabilities, sans
  les étudier. Aucune expérience n'isole ces facteurs. La conclusion (Section 8) reformule cela en
  "commercial models provided stronger privacy defenses", ce qui n'est pas démontré.

### Analyse critique (la mienne, pas celle du papier)
1. **Biais de distribution massif entre membres et non-membres.** Les non-membres sont des
   transformations des membres, dont 30 % ne sont plus du Python (conversion de langage 25 %,
   SQL/Docker/Terraform 5 %) et 40 % ont une logique volontairement cassée. La distance AST de
   0.996 confirme l'écart. Un score de perplexité peut donc séparer "code Python naturel" de "code
   transformé, artificiel ou dans un autre langage" sans aucune information d'appartenance. C'est
   exactement le piège décrit par Duan et al. 2024 (fiche à faire). Aucune baseline sans modèle
   (classifieur de surface) n'est rapportée.
2. **Pas de vérité terrain d'appartenance.** Rien ne garantit que les réponses ProCQA sont dans
   l'entraînement de chaque modèle. Le cas de GPT-2 et DistilGPT-2 est particulier : le papier ne
   discute pas la date de leurs données (WebText, 2019) par rapport aux dates des réponses ProCQA ;
   une partie des "membres" pourrait être postérieure. A vérifier avant de conclure quoi que ce
   soit sur ces modèles.
3. **Inversement, certains non-membres sont peut-être des membres.** Les transformations
   sémantiques et structurelles (30 %) restent proches de code vu ; la conversion vers d'autres
   langages peut produire du code très standard, lui aussi vu. Le label "non-membre" n'est pas
   garanti non plus.
4. **Biais temporel non contrôlé.** Pas de split par date, pas de comparaison avec des réponses
   postérieures aux cutoffs. La règle CodeTrace (baseline "vieux vs récent") ne s'applique même pas
   ici puisque les non-membres ne sont pas datés ; le biais est de nature "transformation" plutôt
   que temporel, mais l'effet est le même : on ne sait pas ce que mesure l'AUC.
5. **Accès aux logprobs d'entrée des API.** Non documenté (voir rubrique 3). Pour les modèles
   fermés (GPT-5, Gemini), il faut vérifier si OpenRouter renvoie vraiment des logprobs sur les
   tokens du prompt ; si ce n'est pas le cas, le score calculé n'est pas celui de l'Algorithme 1.
   A consigner dans docs/model_access.md après vérification, sans présumer de la réponse.
6. **Puissance statistique.** Avec environ 200 échantillons par classe et 70 % en évaluation (soit
   environ 140 par classe), l'écart-type d'une AUC proche de 0.55 est de l'ordre de 0.03 à 0.035
   (approximation Hanley-McNeil, mon calcul), donc un IC à 95 % d'environ plus ou moins 0.07. Les
   différences entre Mistral (0.535), DeepSeek (0.540), LLaMA (0.559) et GPT-5 (0.566) ne sont
   probablement pas significatives, et plusieurs IC incluent 0.5. Un TPR@5%FPR sur environ 140
   négatifs repose sur environ 7 faux positifs : très instable.
7. **Seuil et métriques dépendantes du seuil.** Le seuil 75e/25e percentile fixe précision et F1 ;
   un F1 de 0.666 avec une précision de 0.500 (DeepSeek) suggère un seuil qui classe presque tout
   en membre (rappel élevé). Précision et F1 dépendent aussi du ratio de classes, ici équilibré par
   construction. Le choix de k n'est pas dit fait sur le split de calibration.
8. **k fixe en nombre de tokens** (si c'est bien le cas) : le score dépend de la longueur et du
   tokenizer, qui diffère entre modèles, ce qui rend les comparaisons inter-modèles fragiles.
9. **Section 7 : glissement de problème.** Le code généré par un LLM pour un étudiant n'est pas
   une donnée d'entraînement ; le détecter par faible perplexité relève de la détection de texte
   machine, pas d'une MIA. Le cadre de la Section 3 ne s'applique pas tel quel. De plus : 5 groupes,
   un seul exercice (Titanic, très présent sur le web), vérité terrain auto-déclarée, protocole
   d'attribution à GPT-5 non décrit.
10. **Incohérence apparente du Tableau 1** (vérifié sur le rendu de la p. 7) : "Bisection" fait
    partie du libellé "String manipulation, Guess and Check, Approximations, Bisection" (~1.26M) et
    la ligne à ~569K est "Data structures and algorithms" : c'étaient des artefacts d'extraction.
    En revanche, la somme des fréquences par concept (~6.7M) dépasse bien les ~1.008M
    enregistrements Python annoncés : comptage avec recouvrement probable, non expliqué.
11. **Comparaison limitée** : pas de baseline loss, zlib, Min-K%++ ou voisinage (Mattern et al.),
    alors que le papier se positionne comme extension de Min-K%.

## 7. Réutilisable pour CodeTrace

- **Code et données** : Section 5, "The code and dataset are available at Anonymized GitHub
  Repository". Aucune URL n'apparaît dans l'extraction texte. Lien à demander aux auteurs.
- **Dataset** : ProCQA [17] (Li et al., LREC-COLING 2024), réponses Stack Overflow multi-langages,
  bon candidat de corpus brut. Point clé pour nous : récupérer les dates des réponses (via les IDs
  Stack Overflow ou le dump officiel) pour construire de vrais non-membres postérieurs aux cutoffs.
- **Taxonomie de perturbations** (Algorithme 2) : les stratégies "Semantic" (renommage,
  commentaires) et "Structural" (formatage, réordonnancement) recoupent directement
  src/codetrace/perturb. Les stratégies "Aggressive", "Cross Language" et "Novel Pattern" sont à
  écarter comme non-membres (trop loin de la distribution), éventuellement à garder comme contrôle.
- **Liste de modèles et canal d'accès** : mêmes familles que le sujet CodeTrace, via OpenRouter.
  Leur choix de provider peut économiser une vérification, une fois documenté.
- **Protocole de seuil** (calibration 30 / évaluation 70, percentiles) : réutilisable comme
  baseline de règle de décision, à compléter par TPR@1%FPR et bootstrap.
- **Métrique AST** (tree-edit distance normalisée [28], Song et al. ACL 2024) : utile pour
  quantifier l'amplitude de nos perturbations.

## 8. Idées d'expériences suggérées

1. **Reproduire le Tableau 2 puis le casser** : sur les mêmes membres ProCQA, remplacer les
   synthétiques par des réponses Stack Overflow postérieures aux cutoffs (non-membres naturels) et
   mesurer la chute d'AUC. Ajouter la baseline sans modèle (classifieur de surface sur les features
   du code : langage, validité syntaxique, longueur) pour quantifier le biais de distribution.
2. **AUC stratifiée par stratégie de transformation** : calculer l'AUC membres vs synthétiques
   pour chacune des 5 stratégies séparément. Hypothèse à tester : l'AUC est portée par
   Cross Language et Novel Pattern, et proche de 0.5 pour Semantic et Structural.
3. **Perturbations comme voisins, pas comme non-membres** : utiliser les transformations
   Semantic et Structural à la manière de Mattern et al. 2023 (score = écart entre l'original et
   la moyenne de ses perturbations), ce qui correspond à la question de recherche CodeTrace.
4. **Vérifier l'accès logprobs du prompt via OpenRouter** pour chacun des 5 modèles commerciaux
   (et pour chaque provider sous-jacent), consigner dans docs/model_access.md, avant tout run payant.
5. **Comparer Min-K% à loss, zlib, Min-K%++** sur les mêmes données, avec k en pourcentage et en
   nombre absolu, IC bootstrap, test de DeLong ou permutation entre méthodes.
6. **Modèles à vérité terrain connue** : ajouter des modèles open-weights dont le corpus est public
   (par exemple entraînés sur The Stack) pour avoir de vrais labels membres, ce que le papier n'a
   pas.
7. **Puissance** : estimer la taille d'échantillon nécessaire pour distinguer des AUC de l'ordre de
   0.55 avec un IC de plus ou moins 0.03, et chiffrer le coût API correspondant.

## Questions à poser aux auteurs (encadrants)

1. Comment les logprobs des tokens d'entrée ont-ils été obtenus via OpenRouter, en particulier
   pour GPT-5 et Gemini-2.5-Flash (paramètre, provider, contournement) ?
2. URL du dépôt GitHub (code et données), et implémentation des 5 transformations (règles ou LLM ?).
3. k est-il un nombre de tokens ou un pourcentage ? Sur quel split a-t-il été choisi ?
4. Les dates des réponses ProCQA ont-elles été comparées aux cutoffs des modèles (en particulier
   GPT-2 / DistilGPT-2) ?
5. Section 7 : quel modèle a été scoré, à quelle granularité, et comment l'attribution à GPT-5
   a-t-elle été calculée ?
6. L'Algorithme 1 imprime "si $S \ge \tau$ alors Non-Member", l'inverse de Min-K% : coquille ou
   score négatif ? Et le Tableau 1 compte-t-il des questions avec recouvrement entre concepts ?
