# Fiche : Mattern et al. 2023, Membership Inference Attacks against Language Models via Neighbourhood Comparison

Statut : lue le 2026-11-15. Source de lecture : le PDF local
papers/mia-scores-logprobs/mattern2023-neighbourhood-comparison.pdf est protégé par mot de passe
(l'outil de lecture refuse de l'ouvrir, de même que le PDF de l'ACL Anthology), et le sous-agent
n'avait pas d'accès shell pour lancer pdftotext. Lecture faite sur la version HTML ar5iv
(https://ar5iv.labs.arxiv.org/html/2305.18462), via un outil d'extraction qui résume la page.
Mise à jour 2026-11-15 (session principale) : le PDF s'ouvre avec pdftotext -layout (protection
propriétaire seulement). Les chiffres cités des Tableaux 2 et 3 (p. 6) ont été revérifiés sur
le texte extrait : Neighbour 0.79 / 0.77 / 0.62 en AUC, LOSS 0.64 / 0.60 / 0.52, LiRA base
0.76 / 0.75 / 0.54, LiRA oracle 0.94 / 0.89 / 0.90 ; TPR@1%FPR Neighbour 8.29 % / 7.35 % / 2.32 %.
Les Tableaux 4 à 6 (p. 7-8) et les autres points ci-dessous restent à vérifier.
Conséquences (avant cette mise à jour) :
- les références sont données par section, équation et tableau, **pas par page** (numéros de page
  à ajouter après vérification sur le PDF) ;
- les chiffres des Tableaux 2 à 6 ont été extraits deux fois de manière cohérente, mais sont **à
  revérifier sur le PDF** avant toute citation dans le rapport (en particulier l'alignement des
  colonnes des lignes "Candidate Reference" du Tableau 3, voir rubrique 5) ;
- l'Algorithme 1 est partiellement illisible dans l'extraction : sa description ci-dessous est à
  revérifier.

## 1. Référence

```bibtex
@inproceedings{mattern2023neighbourhood,
  author    = {Mattern, Justus and Mireshghallah, Fatemehsadat and Jin, Zhijing and
               Sch{\"o}lkopf, Bernhard and Sachan, Mrinmaya and Berg-Kirkpatrick, Taylor},
  title     = {Membership Inference Attacks against Language Models via Neighbourhood Comparison},
  booktitle = {Findings of the Association for Computational Linguistics: ACL 2023},
  year      = {2023},
  address   = {Toronto, Canada},
  publisher = {Association for Computational Linguistics},
  pages     = {11330--11343},
  doi       = {10.18653/v1/2023.findings-acl.719},
  url       = {https://aclanthology.org/2023.findings-acl.719},
  eprint    = {2305.18462},
  archivePrefix = {arXiv}
}
```

Affiliations : RWTH Aachen, UC San Diego, MPI for Intelligent Systems (Tübingen), ETH Zürich.
Venue et pages vérifiés sur la notice ACL Anthology.

## 2. Problème et hypothèse (3 phrases)

L'attaque LOSS (seuil sur la perte) a beaucoup de faux positifs car elle ignore la complexité
intrinsèque d'un échantillon ; les attaques à modèle de référence (LiRA) corrigent cela mais
supposent que l'attaquant dispose de données d'entraînement de la même distribution que la cible,
ce qui est souvent irréaliste (Section 1). Les auteurs proposent de remplacer le modèle de
référence par des "voisins" synthétiques du texte cible, générés par un modèle de langue masqué
(Sections 1 et 2). Hypothèse : des voisins quasi identiques reçoivent à peu près la même
probabilité que l'original sous le modèle cible, sauf si l'original a été mémorisé, auquel cas sa
perte est nettement plus faible que celle de ses voisins (Section 1, Section 2.1).

## 3. Méthode

### Score (Section 2.1, équations 1 à 3)

Notations : $f_\theta$ le modèle cible, $\mathcal{L}(f_\theta, x)$ sa perte sur $x$, $\gamma$ un
seuil. Trois attaques sont présentées comme une famille :

LOSS :
$$
A_{f_\theta}(x) = \mathbb{1}\left[\mathcal{L}(f_\theta, x) < \gamma\right]
$$

Calibrée par la difficulté (cas général, $d(x)$ = difficulté estimée de $x$, par exemple via un
modèle de référence pour LiRA) :
$$
A_{f_\theta}(x) = \mathbb{1}\left[\mathcal{L}(f_\theta, x) - d(x) < \gamma\right]
$$

Attaque par voisinage (équation 3), avec $d(x)$ = perte moyenne sur $n$ voisins
$\tilde{x}_1, \dots, \tilde{x}_n$ :
$$
A_{f_\theta}(x) = \mathbb{1}\left[\left(\mathcal{L}(f_\theta, x) - \frac{1}{n}\sum_{i=1}^{n}
\mathcal{L}(f_\theta, \tilde{x}_i)\right) < \gamma\right]
$$

Donc score $S(x) = \mathcal{L}(f_\theta, x) - \frac{1}{n}\sum_i \mathcal{L}(f_\theta, \tilde{x}_i)$ ;
membre si $S(x) < \gamma$ (perte de l'original nettement plus basse que celle de ses voisins).

Précisions :
- **Nombre de voisins** : $n = 100$ dans les expériences principales (Section 3.3) ; ablation
  $n \in \{5, 10, 25, 50, 100\}$ (Tableau 4).
- **Normalisation** : aucune au-delà de la moyenne sur les voisins. Le papier **ne définit pas
  explicitement** $\mathcal{L}(f_\theta, x)$ (perte moyenne par token ou somme ?) : il dit seulement
  que l'attaquant obtient "confidence scores and therefore loss values" (Section 2.1). Pas de
  division par un écart-type des voisins (contrairement à une z-normalisation façon DetectGPT).
  Avec une seule substitution de mot, original et voisins ont presque la même longueur, ce qui
  rend la question moins critique pour eux que pour nous (voir rubrique 7).
- **Seuil** : $\gamma$ est ajusté pour atteindre un FPR cible de 1 %, 0,1 % et 0,01 %, suivant
  Carlini et al. 2021a (Section 3.3). Le papier ne décrit pas de split de calibration séparé :
  le seuil semble fixé directement sur les scores des non-membres évalués (lecture courante en
  TPR@FPR, à confirmer sur le PDF).

### Génération des voisins (Section 2.2, Algorithme 1)

- **Modèle de remplacement** : modèle de langue masqué pré-entraîné, BERT-base (110M) (Sections
  2.2 et 3.3), méthode reprise de Zhou et al. 2019 (substitution lexicale).
- **Astuce de contexte** : au lieu de masquer le mot (ce qui perd son sens), le token original
  reste dans l'entrée et on applique un dropout sur son embedding d'entrée, $p = 0.7$ (Section
  3.3). Pas d'ablation sur $p$ dans ce que j'ai pu lire.
- **Score de substitution** (Section 2.2) : probabilité du candidat renormalisée en excluant
  l'original,
  $$
  p_{\text{swap}}(\hat{w}^{(i)}, \tilde{w}^{(i)}) =
  \frac{p_\theta(\tilde{w} = w^{(i)} \mid x)}{1 - p_\theta(\hat{w} = w^{(i)} \mid x)}
  $$
  (forme recopiée de l'extraction ; les indices exacts sont à revérifier sur le PDF).
- **Algorithme 1** : entrées $x = (w^{(1)}, \dots, w^{(L)})$, $n$, $m$ (nombre de mots remplacés).
  Pour chaque ensemble de $m$ substitutions à des positions distinctes, la "suitability" jointe
  est la somme des $p_{\text{swap}}$ ; on garde les $n$ combinaisons de score maximal. Les auteurs
  prennent "the 100 most likely neighbour samples using one word replacement only" (Section 3.3),
  donc $m = 1$.
- **Taux de remplacement** : $m \in \{1, 2, 3\}$ mots au total par voisin (Tableau 5), pas un
  pourcentage. $m = 1$ est clairement le meilleur (rubrique 5).
- **Contraintes** : les voisins doivent préserver sémantique, structure et syntaxe ; c'est la
  raison donnée pour ne pas utiliser de modèles de paraphrase ou de transfert de style
  (Section 2.2).

### Transposition au code (mon analyse, pas celle du papier)

| Élément Mattern | Transposable au code ? | Commentaire |
|---|---|---|
| Petite perturbation qui préserve le sens | Oui, c'est le coeur de l'idée | Sémantique du code vérifiable (parse, tests, AST), plus strict que pour du texte |
| 1 seul mot remplacé (meilleur, Tableau 5) | Oui | Ex. renommer une seule variable locale, changer un littéral de chaîne ou un commentaire |
| MLM généraliste (BERT) comme générateur | Partiellement | Utiliser un MLM de code (CodeBERT, UniXcoder) ; un swap libre de token casse souvent la syntaxe, il faut filtrer (parse AST) ou restreindre aux identifiants |
| Remplacement d'une occurrence de mot | Pas tel quel | Renommer une seule occurrence d'un identifiant casse le programme ; il faut renommer toutes les occurrences, ce qui fait $m > 1$ tokens modifiés |
| Reformatage (espaces, indentation) | Hors cadre du papier | Ce n'est pas une substitution lexicale ; change la tokenisation et la longueur, donc la normalisation de $\mathcal{L}$ devient critique |
| Réordonnancement d'instructions | Hors cadre | Perturbation structurelle, plus éloignée de l'original que ce que le papier teste |
| Voisins "les plus probables" sous le MLM | Oui | Choisir des renommages plausibles (noms idiomatiques) plutôt qu'aléatoires, sinon la perte des voisins monte pour une raison de naturalité, pas d'appartenance |

### Accès requis

- **Boîte grise** (Section 2.1) : l'attaquant obtient des scores de confiance, donc la perte sur
  un texte arbitraire, sans poids ni gradients.
- Concrètement : la perte $\mathcal{L}(f_\theta, \cdot)$ sur l'original **et sur chacun des $n$
  voisins**, donc les **logprobs des tokens d'entrée** (le texte fourni), pas seulement des tokens
  générés. Inapplicable tel quel à une API qui ne renvoie que les logprobs de complétion.
- Un MLM local (BERT) pour générer les voisins : aucun accès à des données de la distribution
  d'entraînement, c'est l'argument principal du papier.

### Coût (déduit, le papier ne le chiffre pas)

Le papier ne donne ni nombre de requêtes ni coût de calcul (seulement le matériel : GeForce RTX
2080 et Tesla K40, Section 3.3). Déduit de la méthode : **$1 + n$ évaluations de perte du modèle
cible par échantillon, soit 101 avec $n = 100$** (rubrique 3.3), contre 1 pour LOSS ou Min-K%.
S'y ajoute la génération des voisins par BERT (une passe par position avec dropout, coût local).
Pour une API payante facturée aux tokens d'entrée, c'est environ 100 fois le coût d'un score
loss/Min-K%. Le Tableau 4 montre que réduire $n$ dégrade l'attaque (voir rubrique 5).

## 4. Setup expérimental

- **Modèle cible** (Section 3) : GPT-2 base (117M), **fine-tuné** séparément sur chaque dataset.
  Perplexité de validation après fine-tuning : 30.0 (AG News, contre 56.8 avant), 84.7 (Twitter,
  contre 200.3 avant) (Section 3), 55.6 (Wikitext, légende Fig. 3). Nombre d'époques, learning
  rate, longueur des séquences : non indiqués dans ce que j'ai lu.
- **Datasets** (Section 3.1) : AG News (résumés d'articles), Sentiment140 (tweets), Wikitext-103
  (extraits). Aucun code.
- **Membres / non-membres** (Section 3.1) : chaque corpus est coupé en "two disjunct subsets of
  equal size" ; une moitié sert au fine-tuning (membres), l'autre est non-membre. Membres : 60 000
  (News), 150 000 (Twitter), 100 000 (Wikitext), autant de non-membres. Méthode de split non
  précisée (aléatoire présumé).
- **Contrôle du biais de distribution / temporel** : par construction, membres et non-membres
  viennent du même corpus (split IID), donc pas de biais temporel entre les deux classes. Le
  papier ne discute pas ce point explicitement ; il discute le décalage de distribution seulement
  pour les **données des modèles de référence** (Section 3.2, Section 4.2).
- **Baselines** (Section 3.2, Tableau 1) : LOSS ; LiRA avec (i) modèle de référence de base =
  GPT-2 pré-entraîné non fine-tuné, (ii) "candidate" références entraînées sur des données
  proches mais décalées (Candidate 1 : autres catégories AG News + Twitter mental health ;
  Candidate 2 : NewsCatcher + tweets offensants), (iii) "oracle" entraîné sur un autre
  sous-ensemble de la même distribution (60k News, 150k Twitter, 100k Wikipedia). Pas de candidat
  pour Wikipedia (Tableau 1). Les références ont l'architecture de la cible et le meilleur
  checkpoint est choisi "w.r.t attack performance", donc avec le signal d'évaluation (favorable
  aux baselines).
- **Métriques** : TPR à 1 %, 0,1 %, 0,01 % FPR (Tableau 2) et AUC (Tableau 3). Pas d'intervalles de
  confiance, pas de test statistique, pas de seeds rapportés.

## 5. Résultats clés

Tableau 3 (AUC) et Tableau 2 (TPR@1%FPR) ; références marquées * : oracle, hors comparaison
réaliste selon les auteurs.

| Attaque | AUC News | AUC Twitter | AUC Wiki | TPR@1% News | TPR@1% Twitter | TPR@1% Wiki |
|---|---|---|---|---|---|---|
| LOSS | 0.64 | 0.60 | 0.52 | 3.50 % | 2.08 % | 1.06 % |
| LiRA, référence de base | 0.76 | 0.75 | 0.54 | 4.24 % | 5.66 % | 1.21 % |
| LiRA, Candidate 1 | 0.78 | 0.81 | n/a | 4.91 % | 6.49 % | n/a |
| LiRA, Candidate 2 | 0.75 | 0.77 | n/a | 4.76 % | 6.61 % | n/a |
| LiRA, Oracle* | 0.94 | 0.89 | 0.90 | 18.90 % | 13.90 % | 11.70 % |
| **Voisinage (Mattern)** | **0.79** | 0.77 | **0.62** | **8.29 %** | **7.35 %** | **2.32 %** |

Alignement des colonnes des lignes Candidate du Tableau 3 : deux valeurs seulement par ligne, la
colonne Wiki étant vide ; je les ai placées sous News et Twitter, cohérent avec le Tableau 2 et le
Tableau 1 (pas de candidat Wikipedia). A confirmer sur le PDF.

TPR à très faible FPR (Tableau 2) :

| Attaque | News 0.1 % | News 0.01 % | Twitter 0.1 % | Twitter 0.01 % | Wiki 0.1 % | Wiki 0.01 % |
|---|---|---|---|---|---|---|
| LOSS | 0.10 % | 0.01 % | 0.11 % | 0.02 % | 0.11 % | 0.01 % |
| LiRA base | 0.91 % | 0.16 % | 0.98 % | 0.22 % | 0.12 % | 0.01 % |
| LiRA Oracle* | 3.76 % | 0.16 % | 1.59 % | 0.28 % | 3.70 % | 0.12 % |
| Voisinage | 1.73 % | 0.29 % | 1.43 % | 0.28 % | 0.27 % | 0.10 % |

Lecture :
- Le voisinage bat LOSS partout et les LiRA réalistes (base, candidates) en TPR@1% et 0,1 % sur les
  trois datasets (Tableau 2). En AUC, il est au niveau des candidates (0.79 contre 0.78 / 0.75 sur
  News ; 0.77 contre 0.81 / 0.77 sur Twitter, donc battu par Candidate 1) (Tableau 3).
- Il reste loin de l'oracle en AUC et en TPR@1% ; à 0,01 % FPR il l'égale ou le dépasse (News 0.29
  contre 0.16 ; Twitter 0.28 contre 0.28) (Tableau 2). Le texte de la Section 4.1 reconnaît que
  l'attaque ne rejoint pas l'oracle "by a large margin" en général.
- Sur Wikitext, tout est faible : AUC 0.62 pour le voisinage, 0.52 pour LOSS (Tableau 3).

Ablations (Section 4.3) :
- **Nombre de voisins** (Tableau 4, TPR@1%FPR) : News 2.98 % ($n=5$), 4.57 % (10), 6.65 % (25),
  8.19 % (50), 8.29 % (100) ; Twitter 3.93 % à 7.35 % ; Wikipedia 1.57 % à 2.32 %. Gain quasi nul
  entre 50 et 100 sur News, plus marqué sur Twitter.
- **Nombre de mots remplacés** (Tableau 5, TPR@1%FPR) : News 8.29 % ($m=1$), 4.09 % (2), 4.18 %
  (3) ; Twitter 7.35 %, 4.86 %, 4.37 % ; Wikipedia 2.32 %, 1.76 %, 1.44 %. Une seule substitution
  est nettement meilleure.
- **Dépendance à la qualité du modèle de référence** (Section 4.2, Fig. 2 et 3) : LiRA n'est
  meilleure que le voisinage que si la perplexité de validation de la référence est très proche
  de celle de la cible ; argument des auteurs pour la fragilité des attaques à référence.
- **Défense DP-SGD** (Section 5, Tableau 6, AG News) : TPR@1%FPR 8.29 % sans DP ($\varepsilon = \infty$),
  1.52 % à $\varepsilon = 10$, 1.29 % à $\varepsilon = 5$.

## 6. Limites et biais possibles

### Ce que le papier reconnaît (section Limitations, non numérotée)
- Méthode spécifique au texte ; transfert à d'autres modalités non trivial.
- Baselines réimplémentées à partir de leurs descriptions (les résultats dépendent du setup et du
  sur-apprentissage de la cible), donc comparaison possiblement pas parfaitement équitable.
- Section Ethical Considerations : le code n'est pas publié ("will not publicly release"), partagé
  sur demande pour la recherche.

### Analyse critique (la mienne)
1. **Setting fine-tuning, pas pré-entraînement.** Cible = GPT-2 117M fine-tuné sur 60k à 150k
   exemples, perplexité divisée par 2 sur News. C'est un régime de forte mémorisation, très loin
   d'un LLM pré-entraîné sur des milliers de milliards de tokens vus une ou peu de fois. Les AUC
   ne se transposent pas à GPT-5, LLaMA 3.3 ou DeepSeek. Duan et al. 2024 évaluent ce type
   d'attaque en pré-entraînement (fiche à faire, ne rien citer avant).
2. **Absence de biais temporel : force et limite.** Le split IID du même corpus évite le piège
   "vieux vs récent", ce qui rend les AUC interprétables. Mais c'est justement ce que l'on ne peut
   pas reproduire avec un LLM commercial dont on ne contrôle pas les données : pour nous, les
   non-membres seront datés après le cutoff, et le biais revient.
3. **Le voisinage corrige une partie du biais de distribution, pas tout.** La soustraction de la
   perte des voisins calibre la difficulté intrinsèque du texte, ce qui devrait atténuer un décalage
   de distribution global entre membres et non-membres (mon hypothèse, non testée dans le papier).
   Mais si les non-membres récents utilisent des API ou idiomes nouveaux, original et voisins sont
   tous deux "surprenants" et la différence ne dit rien de l'appartenance. A tester.
4. **Définition de la perte non précisée** (moyenne ou somme). Sans importance pour un swap d'un
   mot, critique pour des perturbations qui changent la longueur en tokens.
5. **Seuils fixés sur les données évaluées** (lecture probable, Section 3.3) : TPR@0,01 % FPR sur
   60k à 150k non-membres repose sur 6 à 15 faux positifs ; aucun intervalle de confiance. Les
   écarts à 0,01 % FPR (par exemple 0.28 % contre 0.28 % sur Twitter) ne sont pas interprétables
   sans bootstrap.
6. **Coût** : 101 requêtes par échantillon non discutées alors que l'argument est le réalisme de
   l'attaquant ; prohibitif sur API payante à l'échelle de milliers d'extraits.
7. **Sélection des baselines** : checkpoint des références choisi selon la performance d'attaque
   (Section 3.2), ce qui favorise les baselines ; le voisinage, lui, n'a pas d'ablation sur le
   dropout rapportée.
8. **Un seul modèle cible, une seule taille** : aucune étude de l'effet de la taille ou de
   l'architecture.

## 7. Réutilisable pour CodeTrace

- **Code** : non publié (Ethical Considerations), "on request". Pas de lien GitHub officiel trouvé
  dans le papier. Des réimplémentations existent probablement dans des benchmarks ultérieurs
  (par exemple MIMIR de Duan et al. 2024), à vérifier au moment de lire leur fiche.
- **Dataset** : aucun dataset de code ; AG News, Sentiment140, Wikitext-103 publics mais hors sujet.
- **Protocole réutilisable** :
  - le score $S(x)$ = perte originale moins perte moyenne des voisins, exactement l'idée n°3 de
    notes/maity2026-code-provenance.md (perturbations comme voisins et non comme non-membres) ;
  - la contrainte "petite perturbation, sens préservé, voisins plausibles" et le résultat "1
    substitution > 2 ou 3" (Tableau 5) : guide direct pour calibrer src/codetrace/perturb ;
  - la courbe "TPR en fonction de $n$" (Tableau 4) : protocole pour choisir $n$ sous contrainte de
    budget API ;
  - l'astuce dropout sur l'embedding pour proposer des substituts sans perdre le contexte,
    transposable à un MLM de code pour générer des renommages plausibles ;
  - le reporting en TPR à 1 % et 0,1 % FPR, cohérent avec nos règles (à compléter par bootstrap).
- **Implication accès** (pour docs/model_access.md) : le score exige les logprobs du prompt sur
  $1 + n$ textes ; seuls les modèles open-weights ou un provider exposant les logprobs du prompt
  conviennent.

## 8. Idées d'expériences suggérées

1. **Voisinage sur code, modèle open-weights à vérité terrain connue** : membres tirés d'un corpus
   public d'entraînement (par exemple The Stack pour un modèle qui l'a utilisé), non-membres
   postérieurs ; comparer LOSS, zlib, Min-K%, Min-K%++ et voisinage, AUC et TPR@1/5 % FPR avec IC
   bootstrap.
2. **Ablation par famille de perturbation** : voisins par renommage d'un identifiant (toutes
   occurrences), modification d'un commentaire, modification d'un littéral, reformatage,
   réordonnancement ; mesurer quelle famille donne le meilleur signal, en écho au Tableau 5.
3. **Amplitude de perturbation** : 1, 2, 3 identifiants renommés ; hypothèse issue du Tableau 5 :
   les perturbations minimales gagnent.
4. **Voisins plausibles vs aléatoires** : renommages proposés par un MLM de code (noms idiomatiques)
   contre noms aléatoires (`v1`, `x_83`). Hypothèse : les noms aléatoires augmentent la perte des
   voisins pour tous les extraits et diluent le signal.
5. **Courbe coût / performance** : TPR@1%FPR en fonction de $n \in \{1, 2, 5, 10, 25, 50\}$ ;
   estimer le coût API pour chaque $n$ avant tout run payant. Variante bon marché : un seul voisin
   ou petit $n$ normalisé par l'écart-type (z-score).
6. **Normalisation** : perte moyenne par token contre somme, et z-score sur les voisins, surtout
   pour le reformatage qui change la longueur.
7. **Robustesse au biais temporel** : sur une paire membres anciens / non-membres récents, comparer
   la baseline sans modèle (classifieur de surface sur dates/idiomes), LOSS et voisinage ; tester si
   la calibration par voisins réduit l'écart avec un split IID (hypothèse de la rubrique 6, point 3).
8. **Réanalyse Maity et al.** : appliquer le score de voisinage aux transformations Semantic et
   Structural de leur Algorithme 2, à la place de les étiqueter non-membres.

## Questions ouvertes / à vérifier sur le PDF

1. Numéros de page de chaque élément cité (PDF protégé, non lisible par l'outil).
2. $\mathcal{L}(f_\theta, x)$ : perte moyenne par token ou totale ?
3. Indices exacts de $p_{\text{swap}}$ et détail de l'Algorithme 1.
4. Seuil $\gamma$ : fixé sur les données d'évaluation ou sur un split séparé ?
5. Alignement des colonnes des lignes Candidate du Tableau 3.
