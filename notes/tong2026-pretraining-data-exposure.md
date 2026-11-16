# Fiche : Tong et al. 2026, Pretraining Data Exposure in Large Language Models: A Survey of Membership Inference, Data Contamination, and Security Implications

Statut : lue le 2026-11-16. Source de lecture : le PDF local
papers/contamination/tong2026-pretraining-data-exposure.pdf (11 pages) n'a pas pu être ouvert par
l'outil de lecture du sous-agent, qui l'a cru protégé par mot de passe. C'est faux (`pdfinfo` :
Encrypted no, vérifié le 2026-11-16) : le PDF est lisible avec `pdftotext`. Contrôle fait sur le PDF
le 2026-11-16 : aucune occurrence de AUC ou TPR, Tableau 1 = taxonomie par scénario d'application,
Tableau 2 = comparaison par disponibilité du code, phrase « high false positive rate » sur le code
présente. Lecture
faite sur la version HTML d'arXiv (https://arxiv.org/html/2605.26133v1) via un outil d'extraction
qui résume la page, en cinq passes ciblées (plan et définitions, Section 4.2 et Tableau 1,
Section 5 et Tableau 2, Sections 1, 2, 6 à 8, passages sur le code et les API, bibliographie).
Conséquences :
- les références sont données par section, équation et tableau, **pas par page** (pages à ajouter
  après vérification sur le PDF, par exemple avec `pdftotext -layout`) ;
- les citations entre guillemets sont courtes et viennent de l'extraction : à revérifier mot pour
  mot avant toute reprise dans le rapport ;
- le survey ne contient **aucun résultat chiffré** (vérifié : pas d'AUC, de TPR ni d'accuracy dans
  les Sections 1 à 8 ni dans les Tableaux 1 et 2). La rubrique 5 ne contient donc pas de chiffres.

## 1. Référence

```bibtex
@inproceedings{tong2026pde,
  author        = {Tong, Ziyi and Sun, Feifei and Nguyen, Le Minh},
  title         = {Pretraining Data Exposure in Large Language Models: A Survey of Membership
                   Inference, Data Contamination, and Security Implications},
  booktitle     = {Natural Language Processing and Information Systems (NLDB 2025)},
  year          = {2025},
  doi           = {10.1007/978-3-031-97144-0_14},
  eprint        = {2605.26133},
  archivePrefix = {arXiv},
  note          = {Version arXiv v1 déposée le 2026-05-21, commentaire arXiv "Accepted by NLDB 2025"}
}
```

Affiliation : Japan Advanced Institute of Science and Technology (JAIST), Japon. Licence arXiv :
CC BY-NC-ND 4.0. Venue, DOI Springer et date de dépôt relevés sur la page arXiv abs.
Incohérence d'année : publication NLDB 2025, dépôt arXiv 2026 (déjà signalé dans
docs/etat-de-lart/sources.md). Le nom de fichier du repo garde 2026 ; pour le rapport, citer
plutôt la version NLDB 2025 (à confirmer sur la notice Springer, pages non relevées).

## 2. Problème et hypothèse (3 phrases)

Les corpus de pré-entraînement des LLM sont opaques et issus du web, ce qui pose la question :
une donnée précise a-t-elle été incluse dans le corpus de pré-entraînement d'un LLM (Section 1) ?
Les auteurs appellent ce problème Pretraining Data Exposure (PDE) et soutiennent que la
contamination de données (niveau benchmark / dataset) et les attaques par inférence d'appartenance
(MIA, niveau instance) sont deux faces du même problème, jusque-là étudiées séparément, la MIA
étant traitée comme un sous-cas mineur de la contamination dans les surveys antérieurs (Section 1).
Ce n'est pas un papier à hypothèse testée : la contribution annoncée est (1) un cadre unifié
instance / dataset, (2) une taxonomie des attaques et défenses organisée par scénario applicatif
et type d'utilisateur, (3) une revue des problèmes ouverts (Section 1, contributions).

## 3. Méthode (cadre formel et taxonomie, pas de score propre)

### 3.1 Définitions formelles (Section 3)

Notations : $M$ un LLM, $D_M$ ses données de pré-entraînement, $x, x'$ des instances, $D$ un
dataset, $b(x, x')$ une fonction binaire de correspondance, $f(M, x)$ l'indicateur d'exposition.

**PDE au niveau instance (Section 3.1, Éq. 1)** :
$$
f(M,x)=\begin{cases}1 & \text{si } \exists x' \in D_M,\ b(x,x')=1\\
0 & \text{si } \forall x' \in D_M,\ b(x,x')=0\end{cases}
$$
$x$ est dit "exposed" si $f(M,x)=1$, "unexposed" sinon.

**PDE au niveau dataset (Section 3.2, Éq. 2 et 3)** :
- partiellement exposé : $\exists x \in D,\ f(M,x)=1$ ;
- totalement exposé : $\forall x \in D,\ f(M,x)=1$.

**Exposure score (Section 3.3, Éq. 4)** :
$$
PDE(D,M)=\frac{\sum_{x\in D} f(M,x)}{|D|}
$$
1 = totalement exposé, 0 = non exposé, valeur strictement entre 0 et 1 = partiellement exposé.

Remarques (mon analyse) :
- **$b(x,x')$ n'est jamais défini** dans le texte : on ne sait pas si l'exposition signifie
  correspondance exacte, quasi-doublon ou équivalence sémantique. Seuls indices indirects : la
  Section 2 cite la comparaison "exact-match" [42] comme méthode classique, la Section 6 appelle à
  une détection sémantique "beyond exact matches". Pour CodeTrace, c'est précisément le point à
  fixer : un extrait renommé ou reformaté est-il "exposé" ? Il faudra définir $b$ nous-mêmes
  (exact, quasi-doublon après normalisation, équivalence AST) et le consigner dans
  notes/decisions.md.
- L'Éq. 2 (partiellement exposé, "il existe") inclut le cas totalement exposé, alors que l'Éq. 4
  réserve "partiellement" à $0 < PDE < 1$. Incohérence mineure de définition.
- $f$ est la **vérité terrain** (inconnue de l'attaquant), pas un score de détection. Le survey
  ne formalise pas de détecteur $\hat f$, ni de seuil, ni de métrique d'erreur. L'exposure score
  est donc une quantité à estimer, pas une méthode.

### 3.2 Modèle de menace (Section 4.1)

- Adversaire avec "query access but no access to pretraining data".
- Portée : modèles open-source **et** API commerciales, LLM textuels en anglais.
- Aucune autre précision : le survey ne distingue pas les niveaux d'accès (logprobs du prompt,
  logprobs de complétion seulement, texte seul, poids). Les termes "white-box", "grey-box",
  "logprobs" n'apparaissent pas en Section 2 ; "black-box" apparaît une fois en Section 4.2
  (paraphrases difficiles à détecter "especially in black-box settings").
- Section 2 : les MIA sur LLM exploitent les sorties du modèle [13], des "probability
  distributions" [16, 48], les gradients [34, 55] ou les représentations internes. Seule
  typologie de signaux du papier, non reliée aux méthodes de la Section 4.2.

### 3.3 Taxonomie des stratégies de détection (Section 4.2, Tableau 1)

**Point essentiel pour notre tableau comparatif : la taxonomie n'est pas organisée par
technique.** Elle classe les travaux par **scénario applicatif** et **type d'utilisateur**,
chaque scénario étant associé à un risque de sécurité (Section 4.2, Tableau 1). Les auteurs
présentent ce choix comme plus proche des déploiements réels que les taxonomies antérieures.
Le survey **n'indique ni l'accès requis ni, sauf pour quelques méthodes du Tableau 2, le niveau
instance / dataset** des techniques citées, et ne décrit pas le mécanisme de la plupart
d'entre elles (par exemple ni Min-K% [48] ni le voisinage [35] ne sont expliqués).

Tableau 1 (colonnes : scénario, type d'utilisateur, description, risque, travaux) :

| Scénario | Utilisateur | Risque (résumé) | Travaux cités |
|---|---|---|---|
| Contamination des benchmarks NLP | Développeur de LLM | Évaluation non fiable, mémorisation vs généralisation | [11], [62], [63], [6], [45], [2], [41] |
| Données personnelles issues du crawl web | Utilisateur d'API | Régurgitation de données personnelles | [32], [66], [56] |
| Contenu protégé / propriété intellectuelle | Fournisseur d'API | Sortie de contenu protégé, enjeux légaux | [48], [36], [49], [65], [24] |
| Code et sécurité logicielle | Fournisseur et utilisateur d'API | Sortie de code sous licence violée ou non sûr | [64], [54], [33], [62], [40] |

Détail par famille. Colonne "Accès (survey)" : ce que dit le papier. Colonne "Accès (mon
analyse)" : ma lecture de la méthode d'origine, **non vérifiée dans le survey, à confirmer sur la
fiche du papier source** avant toute citation. Niveau : celui du Tableau 2 quand il existe,
sinon "n.p." (non précisé).

**Famille 1 : contamination de benchmarks (Section 4.2, premier scénario)**

| Technique | Réf. | Définition selon le survey | Accès (survey) | Accès (mon analyse) | Niveau | Avantages / limites selon les auteurs |
|---|---|---|---|---|---|---|
| Analyse de perplexité | Li [28] | Estimer la contamination via la perplexité | n.p. | Logprobs des tokens du texte évalué | n.p. | Limite générale de la famille : paraphrases et contamination partielle difficiles "especially in black-box settings" |
| Tests d'échangeabilité | Oren et al. [41] | Mécanisme d'identification de recouvrement de dataset | n.p. | Log-vraisemblance du benchmark dans l'ordre canonique vs ordres permutés (logprobs de séquence) | Dataset (Tab. 2) | Code dispo selon Tab. 2 |
| ConStat | Dekoninck et al. [9] | Outil statistique de détection par la performance | n.p. | Texte généré seulement (scores sur benchmark vs benchmark de référence) | n.p. | n.p. |
| Investigating contamination (TS-Guessing) | Deng et al. [11] | Cité pour la contamination des benchmarks ; aussi pour "deduplication strategies struggle with semantic equivalence in programming corpora" | n.p. | Texte généré (deviner une partie masquée) | Dataset (Tab. 2) | Code non dispo (Tab. 2) |
| Leak, cheat, repeat | Balloccu et al. [2] | Contamination et mauvaises pratiques d'évaluation des LLM fermés | n.p. | Revue de littérature sur l'usage de LLM fermés, pas un détecteur à proprement parler | Dataset (Tab. 2) | Code non dispo (Tab. 2) |
| Autres cités sans description | [62], [63], [6], [45] (LLMSanitize), [8], [12], [67], [25] | Cités comme travaux du scénario | n.p. | [63] : quantile regression pour accélérer la MIA ; [8] : évasion de la détection ; [12] : CDD (texte généré) | n.p. | Limite : déduplication et n-grammes échouent sur l'équivalence sémantique |

**Famille 2 : données personnelles (Section 4.2, deuxième scénario)**

| Technique | Réf. | Définition selon le survey | Accès (survey) | Niveau | Avantages / limites selon les auteurs |
|---|---|---|---|---|---|
| Analyse de fuite de PII | Lukas et al. [32] | Fuite de données personnelles par mémorisation | n.p. | n.p. | La confidentialité différentielle réduit l'utilité et protège mal les PII rares ou sensibles |
| MemHunter | Wu et al. [60] | Vérification de fuite de PII "dataset-wide" à coût réduit | n.p. | Dataset (d'après la description, pas le Tab. 2) | Avantage : coût de calcul réduit |
| Quantification de la mémorisation | Carlini et al. [4] | Cité pour la mémorisation | n.p. | n.p. | n.p. |
| MIA pour évaluer la pseudonymisation | Vakili et Dalianis [53] | MIA utilisée pour évaluer des données pseudonymisées | n.p. | n.p. | n.p. |
| Privacy backdoors | Wen et al. [57] | Empoisonnement d'un modèle pré-entraîné qui renforce les MIA | n.p. (suppose de contrôler le modèle pré-entraîné) | n.p. | n.p. |
| Autres | [66], [56] | Données synthétiques et vie privée ; risques pour les minorités en unlearning | n.p. | n.p. | n.p. |

**Famille 3 : contenu protégé (Section 4.2, troisième scénario)**

| Technique | Réf. | Définition selon le survey | Accès (survey) | Accès (mon analyse) | Niveau | Avantages / limites selon les auteurs |
|---|---|---|---|---|---|---|
| Détection de données de pré-entraînement (Min-K%) | Shi et al. [48] | Cité seulement (aussi en Section 2 parmi les MIA par "probability distributions") | n.p. | Logprobs des tokens du texte fourni | Instance (Tab. 2) | Code, dataset, benchmark dispo (Tab. 2) |
| EM-MIA | Kim et al. [24] | Méthode espérance-maximisation qui "refines membership probabilities" | n.p. | Logprobs du texte (scores de type MIA raffinés itérativement sur un lot) | Instance (Tab. 2) | Selon les auteurs, excelle sur les données protégées "under experimental setups", sans chiffre |
| SaMIA | Kaneko et al. [23] | Pseudo-vraisemblance par échantillonnage, améliore l'inférence "without internal training dataset access" | Sans accès aux données d'entraînement | Texte généré seulement (échantillons comparés à la suite du texte) | n.p. | n.p. |
| Copyright traps | Meeus et al. [36] | Pièges insérés dans les contenus protégés | n.p. | **Marquage préalable** des données + logprobs/perplexité au test | n.p. | n.p. |
| Mosaic memory | Shilov et al. [49] | Duplication floue dans les copyright traps | n.p. | Marquage préalable | n.p. | n.p. |
| Identifiants uniques | Zhao et al. [65] | Identifiants uniques pour protéger le contenu protégé | n.p. | Marquage préalable | n.p. | n.p. |

Limite générale de la famille selon les auteurs : "no single solution" ne règle à la fois les
problèmes techniques, légaux et éthiques.

**Famille 4 : code et sécurité logicielle (Section 4.2, quatrième scénario)** : voir rubrique 3.4.

**Familles "défense" (Section 5)**, utiles pour la colonne "watermark / marquage" du tableau
comparatif. Le survey les range en mitigation, pas en détection :

| Famille | Réf. | Avantages selon les auteurs | Limites selon les auteurs |
|---|---|---|---|
| Benchmarks dynamiques | [15], [44], [27], [68], [6], [58] ; code : LiveCodeBench [21] ; aussi [3], [7] | Robustesse, favorise la généralisation | Peut limiter reproductibilité et ouverture |
| Benchmarks privés / sécurisés | [20] (chiffrement), [5] (isolation cryptographique) | Intégrité, confidentialité | Même compromis reproductibilité / ouverture |
| Décontamination automatique | AntiLeak-Bench [59], [26], [68] | Passe à l'échelle | Peine sur les paraphrases |
| Watermarking | [43], TextMarker [29] | Appui au droit d'auteur ; [43] réduirait le succès d'attaques d'inversion | Complexité d'entraînement accrue (TextMarker), effet possible sur la généralisation, statut légal incertain, robustesse peu étudiée |
| Machine unlearning | [52], [22], [56], [14], [31] | Suppression a posteriori, "ultimate solution" en principe | Difficile, peut dégrader les performances, efficacité limitée |
| Confidentialité différentielle (citée en Section 4.2, pas en Section 5) | [32] | n.p. | Réduit l'utilité, protège mal les PII rares |

Conclusion des auteurs (Section 5) : aucune méthode ne suffit seule, il faut les combiner.

### 3.4 Ce que le survey dit du code

- Scénario dédié dans le Tableau 1 : modèles entraînés sur des dépôts publics ("e.g., GitHub,
  Stack Overflow"), risque de sortie de code propriétaire, non sûr ou violant une licence ;
  utilisateurs concernés : fournisseur **et** utilisateur d'API (Section 4.2, Tableau 1).
- Méthodes "tailored" citées : CodeMI [54] (MIA pour modèles de complétion de code, c'est
  Wan et al. 2024, déjà dans papers/) et TraWiC [33] (détection d'inclusion de code, déjà dans
  papers/) (Section 4.2, paragraphe 5).
- Métriques citées : "token-level decoding" [39] (caractérisation de la mémorisation de secrets
  au niveau token) et "confidence score calibration" [64] (Zhang et Li 2023, MIA sur modèles
  de code pré-entraînés) (Section 4.2, paragraphe 5).
- Autres travaux code du Tableau 1 : Gotcha [62] (Yang et al.) et CodexLeaks [40] (Copilot).
- Affirmation clé (Section 4.2, paragraphe 5) : la structure déterministe du code favorise la
  mémorisation de contenus sensibles ("credentials, function templates"), ce qui entraîne selon
  les auteurs "a high false positive rate" pour les métriques de MIA. Aucun chiffre ni
  référence attachée à cette phrase. La déduplication peine sur l'équivalence sémantique dans les
  corpus de code (citant [11]).
- Section 6 : le code présente un risque supplémentaire à cause de sa nature déterministe.
- Section 5 : LiveCodeBench [21] comme benchmark dynamique pour le code ; Cao et al. [3] cité pour
  les contre-mesures de contamination dans les modèles de code.
- Aucun watermark spécifique au code n'est cité (ni CoProtector, ni CodeMark, présents dans
  papers/watermarking/).

### 3.5 Ce que le survey dit des API fermées

- Le modèle de menace couvre explicitement les "commercial APIs" (Section 4.1), mais le papier ne
  discute pas ce que ces API exposent (logprobs du prompt ou non, top-k seulement, texte seul).
- Aucune mention de GPT, ChatGPT ou GPT-4 dans le corps du texte (vérifié par recherche dans
  l'extraction). Les modèles fermés n'apparaissent que via des titres de références ([1] Claude,
  [51] Gemini, [2] "closed-source llms", [40] Copilot).
- Seules indications pertinentes pour une API sans logprobs : SaMIA [23] (sans accès aux données
  d'entraînement, par échantillonnage) et la remarque sur la difficulté en "black-box settings".
  **Le survey n'aide pas à répondre à la question critique de CodeTrace** (quels scores sont
  calculables sur OpenAI / Gemini) ; il faut l'établir nous-mêmes dans docs/model_access.md.

### 3.6 Accès requis par le survey lui-même

Sans objet : pas de méthode propre, pas d'expérience.

## 4. Setup expérimental

Aucun. Survey qualitatif : pas de modèle évalué, pas de dataset construit, pas de définition
opérationnelle des membres / non-membres. Le Tableau 2 (Section 5.1) compare seulement la
disponibilité du code, des informations de dataset et de benchmark pour 9 travaux.

## 5. Résultats clés

Pas de résultat chiffré dans le papier (vérifié sur l'ensemble des sections et tableaux de la
version HTML). Seule mention qualitative de performance : EM-MIA [24] "excelling in detecting
copyrighted data under experimental setups" (Section 4.2), sans chiffre.

Tableau 2 (Section 5.1), recopié (✓ = oui, ✗ = non) :

| Méthode | Réf. | Niveau | Type | Code | Infos dataset | Infos benchmark |
|---|---|---|---|---|---|---|
| Balloccu et al., Leak, cheat, repeat | [2] | Dataset | Détection | ✗ | ✗ | ✓ |
| Kim et al., EM-MIA | [24] | Instance | Détection | ✓ | ✓ | ✓ |
| Oren et al., Proving Test Set Contamination | [41] | Dataset | Détection | ✓ | ✓ | ✓ |
| Shi et al., Detecting Pretraining Data | [48] | Instance | Détection | ✓ | ✓ | ✓ |
| Deng et al., Investigating Data Contamination | [11] | Dataset | Détection | ✗ | ✓ | ✓ |
| Mattern et al., Neighbourhood comparison | [35] | Instance | Détection | ✓ | ✓ | ✗ |
| LatestEval | [27] | Dataset | Mitigation | ✓ | ✓ | ✓ |
| AntiLeak-Bench | [59] | Dataset | Mitigation | ✓ | ✓ | ✓ |
| Eldan et Russinovich, Who's Harry Potter? | [14] | Instance | Mitigation | ✗ | ✓ | ✓ |

**Attention** : le Tableau 2 marque le code de Mattern et al. [35] comme disponible, alors que
notre fiche notes/mattern2023-neighbourhood-comparison.md (rubrique 6) relève que Mattern et al.
déclarent ne pas publier leur code ("on request"). Le Tableau 2 n'est donc pas une source fiable
pour la disponibilité du code ; vérifier sur chaque papier.

## 6. Limites et biais possibles

### Ce que le papier reconnaît (Section 8)
- Uniquement les LLM textuels ; exclut les autres types de modèles, le multimodal, le multilingue
  et les langues peu dotées.
- Des travaux pertinents ont pu être omis.

### Défis ouverts listés (Section 6)
1. Détecter les instances paraphrasées ou partiellement contaminées.
2. Détecter les instances à faible occurrence.
3. Aucune approche ne règle seule les aspects techniques, légaux et éthiques.
4. Le code ajoute un risque à cause de sa nature déterministe.

Pistes futures (Section 6) : unlearning sans perte de performance, explicabilité de la
mémorisation, détection au niveau sémantique au-delà des correspondances exactes.

### Analyse critique (la mienne)
1. **Aucune discussion du biais de distribution ni du biais temporel.** Le survey ne traite pas la
   question de la construction des membres / non-membres, ni le fait que des non-membres
   postérieurs au cutoff diffèrent par la distribution (vérifié : sujet absent). Duan et al. 2024
   [13] est cité uniquement comme exemple de MIA "par les sorties" (Section 2), sans mention de
   sa conclusion sur le décalage de distribution. WikiMIA et MIMIR ne sont pas mentionnés. Les
   travaux qui démontent les benchmarks MIA par des baselines "aveugles" (Das et al., Meeus et al.
   SoK, présents dans papers/mia-evaluation/) ne sont pas cités. Pour CodeTrace, le survey ne
   fournit donc **aucune recommandation d'évaluation** ; nos règles (baseline temporelle
   obligatoire, AUC + TPR@1/5 % FPR, bootstrap) viennent d'ailleurs.
2. **Aucune métrique d'évaluation** n'est discutée (ni AUC, ni TPR à faible FPR) ; l'exposure
   score (Éq. 4) est défini sur la vérité terrain, sans lien avec l'erreur d'un détecteur.
3. **Taxonomie par scénario, pas par technique ni par accès** : une même méthode peut relever de
   plusieurs scénarios (Gotcha [62] apparaît en benchmark et en code), et deux méthodes aux
   exigences d'accès opposées (Min-K% qui demande les logprobs du texte, copyright traps qui
   demandent un marquage préalable) sont dans la même case. Inutilisable telle quelle comme
   squelette d'un tableau comparatif technique ; il faut ajouter les axes accès / niveau /
   marquage préalable (proposition en rubrique 7).
4. **Couverture incomplète des techniques MIA de référence** : pas de description des scores loss,
   zlib, Min-K%++, ni des attaques à modèle de référence, ni de dataset inference (Maini et al.
   2024 absent des références), ni des méthodes boîte noire récentes (DE-COP, n-gram coverage,
   PETAL, etc.). Voir la liste des références manquantes en rubrique 7.
5. **Affirmation non étayée sur le code** : "high false positive rate" des MIA sur le code
   (Section 4.2) sans chiffre ni référence attachée à la phrase. Hypothèse intéressante à tester
   chez nous, pas un résultat.
6. **Erreur factuelle probable** dans le Tableau 2 (code de Mattern [35], voir rubrique 5) et
   incohérence de définition Éq. 2 / Éq. 4 (rubrique 3.1). La conclusion (Section 7) parle de
   MIA comme "extraction", alors que le corps du texte parle de détection.
7. **Date** : publié à NLDB 2025, donc la revue de littérature s'arrête vers fin 2024 (références
   les plus récentes en 2025 : [6], [7], [15], [34], [52], [66]) malgré le dépôt arXiv de 2026.

## 7. Réutilisable pour CodeTrace

- **Code / dataset** : aucun (survey). Aucun lien GitHub donné dans le papier. Le Tableau 2 liste
  les travaux avec code disponible (EM-MIA, Oren, Min-K%, LatestEval, AntiLeak-Bench), à
  vérifier sur chaque papier. La bibliothèque LLMSanitize (Ravaut et al. [45], déjà dans papers/)
  est citée : candidate à regarder pour des implémentations de détecteurs de contamination.
- **Formalisme** : reprendre $f(M,x)$, $b(x,x')$ et l'exposure score $PDE(D,M)$ dans notre
  section "définitions", en **définissant explicitement $b$** pour le code. Proposition : trois
  niveaux, exact (octets identiques), normalisé (après suppression commentaires / espaces), et
  sémantique (même AST modulo renommage). Le choix détermine qui est "membre" pour nos
  perturbations.
- **Niveau instance vs dataset** : distinction utile pour notre objectif 4 (critères de décision) :
  décider sur un extrait (MIA) ou sur un dépôt entier (agrégation type dataset inference).
- **Squelette proposé pour le tableau comparatif** (axes du survey + axes manquants) : méthode,
  famille (MIA score / dataset inference / contamination / boîte noire / marquage), niveau
  (instance / dataset), accès requis (logprobs du prompt / logprobs de complétion / texte généré
  seulement / poids ou gradients / marquage préalable des données), besoin d'un modèle ou corpus
  de référence, coût en requêtes par échantillon, testé sur du code (oui / non), scénario du
  Tableau 1 (benchmark / PII / copyright / code), code disponible (vérifié sur le papier source),
  meilleure métrique rapportée.
- **Références citées par le survey absentes de papers/papers.toml** (comparaison par identifiant
  arXiv le 2026-11-16) et qui semblent importantes pour couvrir les techniques :
  - Code, prioritaires :
    - [64] Zhang et Li 2023, Code membership inference for detecting unauthorized data use in
      code pre-trained language models, arXiv 2312.07200 (MIA code, "confidence score
      calibration") ;
    - [39] Nie et al. 2024, Decoding secret memorization in code LLMs through token-level
      characterization, arXiv 2410.08858 ;
    - [3] Cao et al. 2024, Concerned with data contamination? Assessing countermeasures in code
      language model, arXiv 2403.16898.
  - Scores MIA / détection :
    - [16] Fu et al. 2023, SPV-MIA, self-prompt calibration, arXiv 2311.06062 (référence auto
      générée, alternative aux modèles de référence) ;
    - [63] Zhang, Bertran et Roth 2024, Order of magnitude speedups for LLM membership inference,
      arXiv 2409.14513 (coût) ;
    - [55] Wang et al. 2024, Pandora's white-box (boîte blanche, pas d'ID arXiv dans la
      bibliographie) ;
    - [34] Mancera et al. 2025, gradient-based membership inference test (pas d'ID arXiv) ;
    - [38] Mozaffari et al. 2024, Semantic membership inference attack (paraphrases, pas d'ID
      arXiv), pertinent pour nos perturbations sémantiques.
  - Contamination :
    - [28] Li 2023, Estimating contamination via perplexity, arXiv 2309.10677 ;
    - [9] Dekoninck et al. 2024, ConStat, arXiv 2405.16281 (détection par performance, texte
      seul, utile pour les API fermées) ;
    - [8] Dekoninck et al. 2024, Evading data contamination detection is (too) easy, arXiv
      2402.02823 (robustesse des détecteurs) ;
    - [11] Deng et al. 2024, Investigating data contamination in modern benchmarks, arXiv
      2311.09783 (TS-Guessing, texte seul) ;
    - [2] Balloccu et al. 2024, Leak, cheat, repeat, arXiv 2402.03927 (LLM fermés).
  - Marquage préalable :
    - [29] Liu et al. 2023, TextMarker, arXiv 2305.13257 ;
    - [49] Shilov et al. 2024, Mosaic memory, arXiv 2405.15523 ;
    - [65] Zhao et al. 2024, unique identifiers (pas d'ID arXiv) ;
    - [43] Panaitescu-Liess et al. 2024, watermarking vs copyrighted generation, arXiv 2407.17417.
  - Mémorisation / PII, secondaire : [60] MemHunter, arXiv 2412.07261 ; [57] Wen et al. 2024,
    Privacy backdoors, arXiv 2404.01231.
  - Surveys concurrents, secondaire : [7] Cheng et al. 2025, arXiv 2502.14425 ; [10] Deng et al.
    2024, arXiv 2406.14644.
  - Déjà dans papers/ (vérifié) : [4] Carlini 2023, [12] Dong (CDD), [13] Duan, [17] Fu, [21]
    LiveCodeBench, [23] SaMIA, [24] EM-MIA, [33] TraWiC, [35] Mattern, [36] Meeus traps, [40]
    CodexLeaks, [41] Oren, [45] Ravaut, [48] Shi, [54] Wan, [61] Xu, [62] Yang Gotcha.
- **Inversement, techniques importantes absentes du survey** mais présentes dans papers/ : Carlini
  2021 (loss, zlib), Min-K%++, dataset inference (Maini 2024), DE-COP, ReCaLL, DC-PDD, n-gram
  coverage, PETAL, watermarks de code (CoProtector, CodeMark), SoK de Meeus 2025 et blind
  baselines de Das 2024. Le tableau comparatif devra s'appuyer sur ces fiches, pas sur ce survey.

## 8. Idées d'expériences suggérées

1. **Tester l'affirmation "taux de faux positifs élevé sur le code"** (Section 4.2) : sur des
   non-membres certains (code postérieur au cutoff), mesurer la proportion d'extraits très
   "templatés" (boilerplate, getters, imports) classés membres par loss / Min-K%, en fonction d'une
   mesure de prévisibilité du code (zlib, longueur, fréquence des idiomes).
2. **Exposition selon la définition de $b$** : pour un même modèle open-weights et The Stack comme
   vérité terrain, construire les labels avec $b$ exact, normalisé et sémantique, et comparer l'AUC
   des scores. Mesure directe de l'effet "paraphrase / contamination partielle" (défi 1 de la
   Section 6) sur le code.
3. **Faible occurrence** (défi 2 de la Section 6) : stratifier les membres par nombre de copies
   (quasi-doublons) dans le corpus d'entraînement et tracer l'AUC par strate.
4. **Instance vs dataset** : agréger les scores d'instance d'un dépôt entier en un estimateur de
   $PDE(D,M)$ (Éq. 4) ou un test au niveau dataset, et comparer la puissance avec la décision
   extrait par extrait.
5. **Méthodes texte seul pour les API fermées** : SaMIA [23], TS-Guessing [11] et ConStat [9] sont
   cités comme ne nécessitant pas les logprobs internes (mon analyse pour [11] et [9], à vérifier) ;
   candidats pour GPT-5 / Gemini si les logprobs du prompt sont indisponibles.
6. **Benchmarks dynamiques comme source de non-membres** : LiveCodeBench [21] (problèmes datés)
   fournit des non-membres datés, mais avec biais temporel par construction : à coupler avec la
   baseline "vieux vs récent" sans modèle.

## Questions ouvertes / à vérifier sur le PDF

1. Numéros de page de chaque élément cité (PDF protégé, non lisible par l'outil).
2. Formulation exacte de l'Éq. 2 et 3 et de l'Éq. 4 (recopiées de l'extraction HTML).
3. Formulation exacte de la phrase "high false positive rate" et des citations courtes.
4. Pages et volume LNCS de la version NLDB 2025.
