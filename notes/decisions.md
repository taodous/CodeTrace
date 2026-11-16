# Décisions méthodologiques

Une entrée par décision : date, décision, justification, alternatives écartées.

## 2026-11-15 : phase 1 restreinte aux modèles gratuits

**Décision.** La phase 1 (todo P1 à P4) n'utilise que des accès gratuits : modèles open-weights
exécutés en local avec transformers. Les tests réels des API payantes (script
`scripts/check_logprobs.py`) sont reportés à P11, sous réserve d'un budget.

**Justification.**
- Toutes les API visées demandent un paiement ou un abonnement pour la moindre requête (constat de
  l'utilisateur à la création des comptes : OpenRouter, Mistral...).
- La voie gratuite d'OpenRouter ne sert pas : sur 467 modèles du catalogue public, 14 sont `:free`
  (relevé du 2026-11-15, `GET /api/v1/models`). Aucun n'est un modèle du sujet, seuls 3 annoncent
  `logprobs`, et OpenRouter ne donne de toute façon jamais les logprobs du prompt
  (`docs/model_access.md`, [D11]).
- En local, on a les logprobs de chaque token d'entrée, ce qu'exigent loss, zlib, Min-K% et Min-K%++.
- Avec un modèle dont le corpus d'entraînement est public, le label membre est documentable, ce que
  les API fermées ne permettent pas.

**Contrainte matérielle relevée** (nvidia-smi, 2026-11-15) : NVIDIA GeForce RTX 2050, 4 Go de VRAM ;
16 Go de RAM. Cela limite le local à environ 1 à 3B paramètres. Mistral Small 24B, LLaMA 3.3 70B et
DeepSeek-V3 (open-weights, donc gratuits) ne tournent pas sur cette machine.

**Alternatives écartées pour l'instant.**
- Payer les API : pas de budget à ce jour (question posée aux encadrants, todo R1).
- Modèles `:free` d'OpenRouter : pas de logprobs du prompt, pas de corpus d'entraînement connu.
- GPU gratuits en ligne (Colab, Kaggle) pour les modèles 7B à 24B : à évaluer en P1c, pas écartés.
