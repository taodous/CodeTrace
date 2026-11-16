# Mini état de l'art provisoire (checkpoint tuteur)

*Rédigé le 2026-11-16. Base : 12 papiers lus (extraction texte `pdftotext`, lecture ciblée :
résumé, méthode, setup, tableaux de résultats principaux, conclusion) et les 2 fiches déjà faites
(`notes/maity2026-code-provenance.md`, `notes/mattern2023-neighbourhood-comparison.md`).
Règle de sélection : un papier par sous-sujet, pas deux papiers sur la même question.
Ce n'est pas encore une fiche par papier : avant de citer un chiffre dans le rapport, le revérifier
dans le PDF et faire la fiche (`/new-paper`).*

---

## 0. À retenir en 6 phrases (pour le meeting)

1. CodeTrace est un problème de **membership inference (MIA)** sur données de pré-entraînement :
   le code `x` était-il dans le corpus du modèle `M` ?
2. Les scores classiques (loss, zlib, Min-K%, Min-K%++, voisinage) donnent un signal **faible**
   quand membres et non-membres viennent vraiment de la même distribution : AUC proche de 0,5 à
   0,6 sur le texte (Duan 2024) et autour de 0,6 sur le code (CodeSnitch, Li 2025).
3. Beaucoup de « succès » publiés mesurent en fait un **décalage de distribution** (temporel,
   lexical, de transformation) entre membres et non-membres. Le papier de nos encadrants
   (Maity 2026) est exposé à ce biais, car ses non-membres sont des transformations des membres.
4. Les méthodes **comparatives** (original contre voisins perturbés) résistent mieux au biais
   temporel que les scores directs (CodeSnitch, RQ5). C'est un argument fort pour l'idée
   « authentique contre perturbé » de CodeTrace.
5. Une MIA seule **ne prouve pas** qu'un modèle a été entraîné sur un code (Zhang et al. 2025) ;
   pour un verdict fiable il faut agréger au niveau dépôt (dataset inference, Maini 2024) ou
   recourir à des canaris, des watermarks ou de l'extraction.
6. Pour les API fermées (GPT-5, Gemini), pas de logprobs du prompt : il faut des méthodes à partir
   du **texte généré** (n-gram coverage, Hallinan 2025), avec des logprobs d'API non
   déterministes (Chauvin 2026).

---

## 1. Papiers lus et rôle de chacun

| Sous-sujet | Papier lu | Pourquoi celui-là |
|---|---|---|
| Scores sur logprobs | Zhang et al. 2025, **Min-K%++** (ICLR 2025) | État de l'art sans référence ; ses tableaux reprennent loss, zlib, Neighbor, Min-K% sur WikiMIA et MIMIR |
| Voisinage perturbé | Mattern et al. 2023 (fiche existante) | Ancêtre direct de l'idée CodeTrace |
| Biais d'évaluation | Duan et al. 2024, **Do MIAs work on LLMs?** (COLM 2024) | Benchmark MIMIR, explication du biais temporel, cas GitHub |
| Limites de la preuve | Zhang, Das, Kamath, Tramèr 2025, **MIAs cannot prove...** | Pourquoi une MIA n'est pas une preuve ; voies valides |
| Niveau dataset | Maini et al. 2024, **LLM Dataset Inference** | Agrégation de MIA faibles + test statistique |
| Boîte noire (texte seul) | Hallinan et al. 2025, **N-Gram Coverage Attack** (COLM 2025) | MIA sans logprobs, testée sur modèles OpenAI |
| MIA sur code : benchmark | Li et al. 2025/2026, **Are AI Coders Snitches? (CodeSnitch)** | Évaluation propre de 9 méthodes sur 8 LLM de code |
| MIA sur code : perturbation AST | Koohestani et al. 2026, **AST-PAC** | Calibration par voisins syntaxiquement valides : le plus proche de CodeTrace |
| Transformations comme évasion | Yang et al. 2026, **Semantically equivalent code transformations** (ICSE 2026) | Effet du renommage, etc., sur la détection |
| Mémorisation du code | Al-Kaswan et al. 2024, **Traces of memorisation** (ICSE 2024) | Extraction, facteurs de mémorisation du code |
| Contamination de benchmarks | Riddell et al. 2024, **Quantifying contamination (code)** | HumanEval / MBPP présents dans la Pile et The Stack |
| Watermarking / audit proactif | Du et al. 2025, **SoK dataset copyright auditing** | Cadre intrusif / non intrusif |
| Audit d'API par logprobs | Chauvin et al. 2026, **Log probability tracking of LLM APIs** (ICLR 2026) | Ce que valent les logprobs servis par une API |
| Papier des encadrants | Maity et al. 2026 (fiche existante) | Point de départ du sujet |

Non lus volontairement (sujet déjà couvert par un papier lu) : Carlini 2021 et Shi 2024 (repris et
dépassés par Min-K%++), Das 2024 blind baselines et SoK Meeus 2025 (même message que Duan),
SynPrune, AdvPrompt-MIA (Jiang 2025), CodeMI (Wan 2024), GotCha, TraWiC (couverts par CodeSnitch
et AST-PAC), les autres surveys. **Ne rien affirmer sur leur contenu** au-delà de ce que CodeSnitch
en dit (il évalue CodeMI et AdvPrompt-MIA, voir section 4).

---

## 2. Vocabulaire minimal

- **Membre / non-membre** : échantillon présent ou non dans le corpus d'entraînement.
- **Accès boîte grise** : on obtient les logprobs (ou logits) des tokens de l'**entrée**. C'est ce
  que supposent loss, zlib, Min-K%, Min-K%++, voisinage.
- **Accès boîte noire** : on n'a que le texte généré (éventuellement les logprobs des tokens
  générés, top-k).
- **AUC-ROC** : probabilité qu'un membre ait un meilleur score qu'un non-membre (0,5 = hasard).
- **TPR@x%FPR** : taux de détection quand on n'accepte que x % de fausses accusations. Métrique
  pertinente pour un audit, car une fausse accusation coûte cher.
- **Dataset inference** : décider pour un *ensemble* (un dépôt) plutôt que pour un extrait.
- **Clones de code Type 1 à 3** : identique sauf formatage / renommage / modifications de
  statements. Sert à définir des « quasi-membres ».

---

## 3. Les scores fondés sur les logprobs

Formulation commune : on calcule un score `s(x; M)` puis on seuille.

| Score | Idée | Référence |
|---|---|---|
| Loss / perplexité | Un membre a une perte plus faible | Yeom 2018, repris partout |
| zlib | Loss divisée par la taille compressée zlib de `x` (corrige la difficulté intrinsèque) | Carlini 2021 |
| Référence | Loss du modèle cible moins loss d'un petit modèle de référence | Carlini 2021 |
| Voisinage | Loss de `x` moins loss moyenne de voisins perturbés de `x` | Mattern 2023 |
| Min-K% | Moyenne des k % log-probas de tokens les plus faibles | Shi 2024 |
| **Min-K%++** | Pour chaque token : `(log p(x_t) − μ) / σ`, où μ et σ sont la moyenne et l'écart-type de log p sur **tout le vocabulaire** au même contexte ; puis moyenne des k % plus faibles | Zhang 2025 |

**Min-K%++ (lu).** Justification théorique : l'entraînement par maximum de vraisemblance pousse les
échantillons d'entraînement vers des maxima locaux de la vraisemblance ; on teste donc si le token
observé est un mode de la distribution conditionnelle. Résultats :
- WikiMIA (split temporel) : +6,2 à +10,5 points d'AUC sur Min-K% selon la longueur.
- MIMIR (Pile, split IID, beaucoup plus dur) : gains faibles. Moyenne sur 7 domaines pour
  Pythia-12B : 58,7 contre 55,9 pour Min-K% et 54,9 pour Loss (Tableau 2).
- **Sous-ensemble GitHub de MIMIR** : Loss 74,0, Min-K% 74,3, Min-K%++ 74,2 sur Pythia-12B. Aucun
  gain sur le code. Et cette AUC élevée sur GitHub est un artefact (voir Duan, section 4).
- Point pratique pour nous : Min-K%++ exige la **distribution complète sur le vocabulaire** à
  chaque position. Impossible via une API qui ne renvoie que le top-20, même pour la complétion.
  Réservé aux modèles locaux.

**Voisinage, Mattern 2023 (fiche).** Voisins générés par BERT (1 mot remplacé), 100 voisins.
Testé seulement en **fine-tuning** (GPT-2 117M fine-tuné), régime de forte mémorisation : AUC 0,79
(News), 0,77 (Twitter), 0,62 (Wikipedia). Ces chiffres ne se transposent pas au pré-entraînement :
sur MIMIR, Neighbor est à environ 52 à 54 d'AUC en moyenne (Tableau 2 de Min-K%++).

---

## 4. Le problème central : évaluer honnêtement

### Duan et al. 2024 (lu)
- Benchmark **MIMIR** : Pythia 160M à 12B, membres = train de la Pile, non-membres = test de la
  Pile (même distribution, dédupliqués).
- Résultat : **AUC < 0,6 pour presque tous les domaines et toutes les attaques**. Deux causes :
  énorme corpus vu environ une fois, et frontière floue (les non-membres partagent beaucoup de
  7-grammes avec des membres).
- Le **biais temporel** explique les bons scores ailleurs : sur Wikipedia, non-membres naturels à
  39,3 % de recouvrement 7-grammes contre 13,9 % pour des non-membres décalés dans le temps, et
  l'AUC monte nettement avec ces derniers. Un seuil calibré sur des non-membres récents « teste le
  décalage temporel plutôt que l'appartenance ».
- **GitHub est l'exception (AUC environ 0,70 avec zlib) et c'est un artefact** (annexe B.3) : le
  code a un recouvrement 7-grammes moyen de 76,9 % (licences, signatures, syntaxe répétitive) ; le
  filtre de décontamination (80 % de 13-grammes) ne garde que des non-membres atypiques, faciles à
  séparer. Leçon directe pour CodeTrace : **le code est le domaine où la frontière membre /
  non-membre est la plus floue**, et toute déduplication change la difficulté du benchmark.
- **Membres modifiés** : remplacer 1 seul token d'un membre suffit pour que LOSS le classe comme
  non-membre. Les MIA testent l'appartenance *exacte*. Or pour un audit de code, une version
  renommée ou reformatée devrait compter comme « vue ».
- Autres constats : l'AUC croît avec la taille du modèle ; la déduplication du corpus la fait
  baisser.

### Zhang, Das, Kamath, Tramèr 2025 (lu, papier de position)
- Pour prouver « ce modèle a été entraîné sur mes données », il faut borner le **taux de faux
  positifs sous H0** (modèle non entraîné sur `x`). C'est impossible pour un modèle de production :
  on ne peut pas réentraîner sans `x`, ni échantillonner la distribution nulle.
- Les trois parades courantes sont jugées non valides : non-membres collectés après le cutoff
  (biais de distribution), non-membres « débiaisés » (puissance trop faible, très peu applicable),
  contrefactuels non publiés (ignorent l'effet causal de la publication sur le reste du web).
- Test valide proposé : un **test de rang**. Si `x` a été tiré **uniformément au hasard** dans un
  ensemble `X` avant publication, la probabilité que `x` soit classé dans les k premiers de `X` est
  au plus `k/|X|` sous H0 (Lemme 1). Cas où c'est vrai : **canaris aléatoires**, **watermarks**,
  **extraction** de longs passages.
- **Conséquence directe pour CodeTrace** : « comparer l'authentique à ses variantes perturbées »
  revient à un test de rang de `x` parmi `{x, variantes}`. Mais `x` n'a **pas** été tiré au hasard
  parmi ses variantes : la version authentique (noms idiomatiques, style humain) est *a priori*
  plus probable, même pour un modèle qui ne l'a jamais vue. La borne `k/|X|` ne s'applique pas. Il
  faut donc **calibrer le score sur du vrai code non-membre** passé par la même chaîne de
  perturbations. C'est la baseline la plus importante de notre protocole.

### Maini et al. 2024 (lu)
- Même constat : les MIA par extrait détectent surtout un décalage de distribution, et aucune MIA
  ne marche sur tous les domaines.
- Proposition : **dataset inference**. On a un ensemble suspect et un ensemble de validation IID
  privé (non publié). On calcule 52 features MIA, on apprend une régression linéaire sur une
  moitié, puis on fait un **t-test** sur l'autre moitié, avec p-values combinées sur 10 seeds.
- Résultat : sur tous les sous-ensembles de la Pile (Pythia-12B), p < 0,1 avec **1000 séquences**,
  et aucun faux positif quand on compare deux moitiés de validation.
- Hypothèse forte : disposer de données IID **jamais publiées** du même auteur. Pour du code :
  branches privées, commits non poussés, code écrit après le cutoff dans le même dépôt (mais alors
  on retombe sur le décalage temporel).
- Pour CodeTrace : c'est le bon niveau pour la question « mon dépôt a-t-il servi ? ». L'agrégation
  au niveau dépôt peut transformer un signal faible par fonction (AUC 0,6) en verdict
  significatif.

---

## 5. Spécifique au code

### CodeSnitch, Li et al. (lu) : le benchmark de référence pour nous
- **Labels documentés** : membres = fonctions tirées de **The Stack** (corpus documenté de
  StarCoder) et du corpus DeepSeek-Coder ; non-membres = fonctions de dépôts > 10 000 étoiles
  **créés après le 1er janvier 2024** (ou appelant des API apparues après). 1600 + 1600 fonctions
  par langage, Python, Java, C++, déduplication par signature et audit de quasi-doublons.
  Attention : pour CodeLlama, l'appartenance n'est pas garantie (les auteurs le disent).
- 8 modèles (SantaCoder, StarCoder2 3B/7B, CodeLlama 7B/13B, DeepSeekCoder 1.3B/6.7B/33B),
  9 méthodes, 10 seeds, IC bootstrap.
- **Résultats (Python, AUC moyenne)** : PPL 0,612 ; zlib 0,589 ; Min-30% 0,608 ; Min-30%++ 0,595 ;
  Neighbor (voisins CodeT5+) 0,574 ; CodeMI 0,511 ; AdvPrompt-MIA 0,565 ; ReCaLL 0,796.
  TPR@5%FPR autour de 0,10 pour les scores directs.
- **Pourquoi Min-K% échoue sur le code** : les tokens de la première déclaration d'un nom de
  variable ont une proba faible chez les membres comme chez les non-membres, et Min-K% sélectionne
  justement ces tokens. zlib aussi est moins bon que PPL : la compressibilité ne capte pas la
  complexité du code.
- **ReCaLL à 0,80 est suspect, et les auteurs l'analysent eux-mêmes** : les 12 préfixes
  « non-membres » partagent des n-grammes avec les non-membres testés (même période), pas avec les
  membres. Le score exploite donc en partie la proximité temporelle.
- **RQ5, sensibilité au décalage temporel (résultat clé)** : si l'on prend des non-membres plus
  récents (fin 2025, puis 2026), les scores directs montent artificiellement (PPL 0,578 puis 0,629
  puis 0,738), alors que **Neighbor reste stable (0,574 ; 0,567 ; 0,564)**. La comparaison à des
  voisins annule la nouveauté que le candidat et ses voisins partagent. C'est le meilleur argument
  de la littérature pour l'approche « authentique contre perturbé ».
- Mutations (clones Type 1 à 3) : toutes les méthodes se dégradent ; avec la mutation hybride
  (renommage + statements), environ 0,55 d'AUC.

### AST-PAC, Koohestani et al. 2026 (lu, papier court exploratoire)
- Données : sous-ensemble Java de **The Heap**, stratifié en membres, **quasi-membres** (Jaccard
  ≥ 0,7 via MinHash) et non-membres. Modèles 3 à 7B : Mellum-4B, StarCoder2-3B/7B, SmolLM3-3B
  (généraliste, contrôle).
- PAC (calibration par voisins à tokens échangés) bat Loss sur les modèles spécialisés code ;
  AUC entre environ 0,57 et 0,71 selon le modèle. Les modèles spécialisés code sont plus
  vulnérables que le généraliste.
- **Les quasi-membres sont détectés comme les membres exacts** (StarCoder2, PAC : 0,663 contre
  0,664) : la refactorisation légère n'efface pas le signal.
- Facteurs : code riche en identifiants / commentaires (ratio alphanumérique élevé) et fichiers
  petits à moyens = plus détectables ; gros fichiers complexes = moins.
- AST-PAC remplace les échanges de tokens (qui cassent la syntaxe) par des **échanges de nœuds AST
  de même catégorie** (Tree-Sitter). Mieux sur les gros fichiers, moins bien sur les petits (trop
  peu de mutations) et sur le code riche en texte. Leçon : la **qualité des voisins** est un
  levier majeur, et l'amplitude de perturbation doit être contrôlée (elle varie avec la taille).

### Yang et al. 2026, transformations sémantiquement équivalentes (lu)
- Cadre : un développeur malveillant transforme du code sous licence **avant fine-tuning** pour
  échapper à l'audit. 23 règles Java, 8 modèles fine-tunés (CodeGPT à CodeLlama-7B).
- Les modèles entraînés sur code transformé gardent leurs performances (au plus 1,5 % de perte).
- **RenameVariable** est la règle la plus efficace : 10,19 % de détection MIA en moins sur
  deepseek-coder-1.3b. Combiner les règles n'ajoute rien. Analyse causale (SCM) cohérente.
- Pour CodeTrace : le renommage des identifiants est la perturbation qui touche le plus la
  « mémoire » du modèle. C'est donc à la fois la perturbation la plus informative pour fabriquer
  des voisins et la principale menace d'évasion. Attention : c'est du fine-tuning, pas du
  pré-entraînement.

### Al-Kaswan et al. 2024, mémorisation (lu en partie)
- Extraction (préfixe de 50 tokens, on regarde si le suffixe de 50 tokens est régénéré) sur des
  spans issus de fichiers ayant au moins 5 doublons sur GitHub : 47 % des échantillons jugés
  extractibles sont extraits de CodeGen-Mono-16B.
- La mémorisation croît avec la taille ; les **data carriers** (dictionnaires, constantes, données)
  sont plus mémorisés que le code ou la documentation ; des architectures différentes mémorisent
  des échantillons différents.
- Pour CodeTrace : la **duplication** est le facteur principal. Il faut stratifier les résultats
  par nombre de copies du code sur GitHub et par type de contenu.

### Riddell et al. 2024, contamination (lu en partie)
- Recherche des solutions de HumanEval et MBPP dans la Pile et The Stack (similarité de surface et
  sémantique) : une part importante est présente, et les modèles réussissent mieux sur les
  problèmes déjà vus. Les approches à base de probabilités marchent surtout quand il y a plusieurs
  copies, peu pour une seule (ce qu'ils disent de la littérature).
- Pour CodeTrace : ne pas utiliser HumanEval / MBPP comme non-membres ; ce sont plutôt des membres
  probables.

---

## 6. Modèles fermés et API

### Hallinan et al. 2025, N-Gram Coverage Attack (lu)
- On coupe le document, on donne le préfixe, on **échantillonne plusieurs continuations**, on
  mesure le recouvrement en n-grammes avec le vrai suffixe, on agrège. Texte seul, aucun logprob.
- Fait mieux que la seule autre baseline boîte noire (DE-COP) et atteint environ 91 à 95 % de la
  performance des méthodes boîte grise sur WikiMIA avec LLaMA ; la performance augmente avec le
  nombre de générations (budget).
- Nouveau benchmark WikiMIA2024 Hard (deux versions du même article, avant 2017 et après 2024)
  pour réduire le biais de sujet. Conclusion des auteurs : GPT-4o est plus robuste que les
  anciens modèles.
- Limite à garder en tête : les benchmarks restent temporels (WikiMIA, BookMIA), donc exposés à la
  critique de Duan.
- Pour CodeTrace : c'est la voie naturelle pour GPT-5 et Gemini. Préfixe de fonction, on génère
  la suite, on compare au vrai corps (n-grammes, ou mieux une similarité de code type CodeBLEU /
  AST), et on compare au même score sur les variantes perturbées. Coût = nombre de générations.

### Chauvin et al. 2026, Log probability tracking (lu en partie)
- Les logprobs renvoyés par les API sont **non déterministes**, mais un simple test statistique sur
  leur moyenne suffit à détecter un changement de modèle aussi petit qu'une étape de
  fine-tuning, avec 1 token d'entrée et 1 de sortie (environ 1000 fois moins cher que les méthodes
  existantes).
- Ils trouvent que 23 % des endpoints joignables d'OpenRouter renvoient des logprobs.
- Pour CodeTrace : si on utilise des logprobs d'API, il faut répéter les requêtes et traiter la
  variance ; et vérifier que le modèle servi ne change pas pendant la campagne (cf. l'alerte
  Gemini 2.5 Flash dans `docs/model_access.md`).

### Rappel de nos propres vérifications (`docs/model_access.md`, 2026-11-15)
Aucune des API du sujet ne donne les logprobs du **prompt** via OpenRouter ; Mistral (paramètre
`prompt_logprobs`) et Together (`echo`) en documentent. Phase 1 = modèles locaux (décision du
2026-11-15).

---

## 7. Approche proactive : watermarks et canaris (SoK Du et al. 2025, lu en partie)
- Deux familles d'audit : **intrusif** (on modifie les données avant publication : watermark,
  backdoor, canari) et **non intrusif** (on n'y touche pas : MIA, empreintes). La majorité des
  travaux portent sur l'image et la classification.
- Seul l'intrusif donne une preuve statistiquement solide (cf. Zhang 2025). Mais il ne s'applique
  pas au code **déjà publié**, qui est la cible de CodeTrace. CodeTrace est non intrusif : on
  produit un **indice**, pas une preuve.

---

## 8. Le papier des encadrants vu à travers cette littérature (fiche Maity 2026)
- Min-K% sur des réponses Stack Overflow (ProCQA) supposées membres, contre des **non-membres
  synthétiques** obtenus par 5 transformations (dont 25 % de conversion vers un autre langage et
  40 % de transformations « agressives » qui cassent la logique).
- AUC de 0,535 à 0,654 pour les modèles commerciaux, environ 200 échantillons par classe, pas
  d'intervalle de confiance.
- Lecture à la lumière de Duan et CodeSnitch : les non-membres diffèrent des membres par
  construction (autre langage, code artificiel), donc l'AUC peut mesurer « naturel contre
  transformé » plutôt que l'appartenance. Le CodeSnitch RQ5 montre qu'un score direct comme Min-K%
  est justement sensible à ce genre de décalage.
- Mais l'intuition du papier rejoint celle de CodeTrace : utiliser les transformations
  « Semantic » et « Structural » comme **voisins** (score relatif), pas comme non-membres.
- Questions ouvertes déjà listées dans la fiche (accès aux logprobs du prompt via OpenRouter pour
  GPT-5 et Gemini, sens du seuil dans l'Algorithme 1, k en nombre ou en pourcentage, URL du code).

---

## 9. Positionnement provisoire de CodeTrace

**Ce qui est établi** : signal par extrait faible sur le code (AUC environ 0,6) ; scores directs
sensibles au décalage temporel ; comparaisons à des voisins plus stables ; renommage =
perturbation la plus influente ; duplication et taille du modèle augmentent le signal.

**Lacune exploitable** : personne (dans ce qu'on a lu) ne fait systématiquement, sur des LLM
généralistes récents ouverts **et** fermés :
1. un score « authentique contre variantes **sémantiquement équivalentes** » (renommage,
   formatage, réordonnancement, commentaires), avec des voisins valides (AST) et une amplitude
   contrôlée ;
2. **calibré** sur du vrai code non-membre passé par la même chaîne (réponse à Zhang 2025) ;
3. agrégé au **niveau dépôt** avec un test statistique (Maini 2024) ;
4. avec une variante boîte noire par complétion pour GPT-5 / Gemini (Hallinan 2025) ;
5. stratifié par type de code (langage, duplication, ratio identifiants / commentaires, taille).

**Protocole minimal qui en découle** (à valider en plan mode avant de coder) :
- Modèles locaux à corpus connu (StarCoder2 / The Stack, Pythia / la Pile) en phase 1.
- Membres : The Stack (dates et IDs documentés). Non-membres : dépôts créés après le cutoff
  (méthode CodeSnitch) et/ou The Heap (à lire).
- Baselines obligatoires : classifieur aveugle sans modèle (vieux contre récent), loss, zlib,
  Min-K%, Min-K%++, Neighbor.
- Métriques : AUC, TPR@1% et 5% FPR, IC bootstrap, test de DeLong ou permutation.
- Ablation par type de perturbation (renommage seul, formatage seul, etc.).

---

## 10. Questions à poser au tuteur
1. Accès aux logprobs du prompt pour GPT-5 et Gemini dans Maity 2026 : comment ont-ils été obtenus ?
2. Êtes-vous d'accord pour que la contribution principale soit le **score relatif** (authentique
   contre variantes équivalentes) plutôt qu'un score direct type Min-K% ?
3. Niveau visé : verdict par extrait, ou par dépôt (dataset inference) ? Le second est plus
   défendable statistiquement.
4. Les non-membres synthétiques du papier : faut-il les garder comme contrôle, ou passer à des
   non-membres naturels datés après le cutoff ?
5. Budget API (et GPU) pour la phase avec les modèles du sujet ; est-ce acceptable de commencer
   par StarCoder2 / Pythia en local, dont les corpus sont publics ?
6. Le papier « Auditing Black-Box LLM APIs via Token Probabilities and Data Provenance » de
   l'équipe : référence exacte et PDF.

---

## Prochaines lectures conseillées (une par sous-sujet manquant)
- **The Heap** (dataset de non-membres pour le code, utilisé par AST-PAC) : pas dans `papers/`,
  à ajouter.
- **SynPrune** (Li 2026) : retirer les tokens imposés par la syntaxe, complète l'analyse de
  l'échec de Min-K% sur le code.
- **Das et al. 2024, blind baselines** : pour construire notre baseline sans modèle.
- **ReCaLL** (Xie 2024) : meilleure méthode de CodeSnitch, à comprendre pour la critiquer.
