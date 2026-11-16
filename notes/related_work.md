# Related work

Tableau comparatif, rempli par /new-paper. Une ligne par papier ayant une fiche dans notes/.

| Papier | Méthode | Accès requis | Modèles testés | Données code ? | Meilleure AUC | Limite principale | Fiche |
|---|---|---|---|---|---|---|---|
| Maity et al. 2026 (arXiv 2611.09177) | Min-K% (k=10) + non-membres synthétiques par transformation de code (Algo. 2), seuil par percentiles | logprobs des tokens d'entrée (HF pour les gratuits ; OpenRouter pour les payants, mécanisme non documenté) | DialoGPT-medium/large, GPT-2, DistilGPT-2 ; GPT-5, Gemini-2.5-Flash, Mistral-Small-24B-Instruct, DeepSeek-V3, LLaMA-3.3-70B-Instruct | oui (Python, ProCQA/Stack Overflow ; notebooks étudiants) | 0.713 (DistilGPT-2) ; 0.654 chez les payants (Gemini-2.5-Flash) (Tab. 2) | non-membres = transformations éloignées (30 % hors Python), sans contrôle du biais de distribution ni vérification du cutoff ; pas d'IC | [fiche](maity2026-code-provenance.md) |
| Mattern et al. 2023 (arXiv 2305.18462, Findings ACL 2023) | Attaque par voisinage : perte(x) moins perte moyenne de n = 100 voisins (BERT, 1 mot remplacé), seuil réglé à un FPR cible | logprobs des tokens d'entrée sur 1 + n textes (101 évaluations par échantillon, déduit), MLM local, pas de données de référence | GPT-2 117M fine-tuné (AG News, Sentiment140, Wikitext-103) | non | 0.79 sur AG News (Tab. 3, p. 6) ; TPR@1%FPR 8.29 % (Tab. 2) | fine-tuning d'un petit modèle avec split IID, non testé en pré-entraînement ni sur du code ; coût x100 en requêtes ; pas d'IC | [fiche](mattern2023-neighbourhood-comparison.md) |
