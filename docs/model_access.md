# Accès aux modèles

Vérification documentaire faite le **2026-11-15** (todo P1). **Aucun test réel n'a encore été fait**
(il faut les clés API, voir « Tests réels à faire »). Chaque case indique sa source ; « ? » = non établi.

Rappel du besoin : loss, zlib, Min-K% et Min-K%++ exigent les logprobs **des tokens du code fourni
en entrée** (« logprobs prompt »). Les logprobs de **complétion** ne servent qu'aux méthodes de repli
(scorer une complétion du code, méthodes boîte noire).

## Restriction aux accès gratuits (2026-11-15)

Toutes les API ci-dessous sont payantes : la phase 1 se fait en local, sur des modèles open-weights
(décision dans `notes/decisions.md`). Les tableaux suivants restent valables pour P11.

Modèles `:free` d'OpenRouter (catalogue public, relevé du 2026-11-15) : 14 sur 467, aucun modèle du
sujet. Seuls `liquid/lfm-3-1.7b:free`, `particle-ai/particle-1:free` et `recursive/flint-v1.0:free`
annoncent `logprobs`, et ce sont des logprobs de complétion seulement [D11]. Inutilisables pour Min-K%.

Machine locale : RTX 2050 (4 Go de VRAM), 16 Go de RAM, soit environ 1 à 3B paramètres. Modèles
locaux retenus : à remplir en P1a (nom, taille, licence, corpus d'entraînement, cutoff).

## Synthèse par modèle du sujet

| Modèle | Accès | Logprobs complétion | Logprobs prompt | Top-k max | Coût (1M in / out) | Cutoff | Source + date |
|---|---|---|---|---|---|---|---|
| GPT-5 (`gpt-5-2025-08-07`) | API fermée (OpenAI) | **Probablement non** [D1] | **Non** [D2] | 20 si dispo | 1,25 $ / 10 $ [D3] | 30 sept. 2024 [D3] | doc OpenAI, 2026-11-15 |
| Gemini 2.5 Flash | API fermée (Google) | Oui via `responseLogprobs` [D4], mais signalé « not enabled » sur l'API Gemini à clé, fonctionne sur Vertex AI [F1] | **Non** (le résultat ne couvre que les tokens générés) [D4] | 20 [D4] | 0,30 $ / 2,50 $ (OpenRouter) [D7] | janv. 2025 [D5] | doc Google, 2026-11-15 |
| Mistral Small 24B | Open-weights (Apache 2.0) + API Mistral | Oui (`logprobs`) [D6] | **Paramètre `prompt_logprobs` documenté** sur l'API Mistral [D6] ; en local : oui | ? | 0,05 $ / 0,08 $ (2501) à 0,10 $ / 0,30 $ (3.2) via OpenRouter [D7] | non publié | doc Mistral + OpenRouter, 2026-11-15 |
| LLaMA 3.3 70B Instruct | Open-weights (licence Llama 3.3, gated) | Oui (OpenRouter, Together) [D7, D8] | **Oui via Together `echo` + `logprobs`** [D8] ; en local : oui | 20 (OpenRouter) | 0,71 $ / 0,71 $ (OpenRouter) [D7] | déc. 2023 [D9] | doc Together + carte Meta, 2026-11-15 |
| DeepSeek-V3 | Open-weights (MIT, 671B MoE) + API DeepSeek | Oui (`logprobs`, `top_logprobs` ≤ 20) [D10] | **Non** sur l'API DeepSeek (sortie seulement) [D10] ; en local : oui mais modèle énorme | 20 | 0,29 $ / 1,14 $ (`deepseek-chat-v3-0324`, OpenRouter) [D7] | non publié | doc DeepSeek, 2026-11-15 |

### OpenRouter (voie utilisée par Maity et al. 2026)

- Pas de paramètre `echo` dans la référence API : les logprobs ne portent que sur les tokens générés [D11].
- Catalogue public `GET /api/v1/models`, champ `supported_parameters`, relevé le 2026-11-15 [D7] :

| ID OpenRouter | `logprobs` | `top_logprobs` |
|---|---|---|
| `openai/gpt-5` | **non** | **non** |
| `google/gemini-2.5-flash` | **non** | **non** |
| `mistralai/mistral-small-24b-instruct-2501` | non | non |
| `mistralai/mistral-small-3.1-24b-instruct` | oui | oui |
| `mistralai/mistral-small-3.2-24b-instruct` | oui | oui |
| `deepseek/deepseek-chat` | non | non |
| `deepseek/deepseek-chat-v3-0324` | oui | oui |
| `meta-llama/llama-3.3-70b-instruct` | oui | oui |

Un paramètre non supporté est **ignoré sans erreur** par OpenRouter [D11] : une réponse sans logprobs
peut donc passer inaperçue. Utiliser `provider: {"require_parameters": true}` pour l'interdire.

**Conséquence pour la fiche Maity** : d'après le catalogue actuel, ni GPT-5 ni Gemini 2.5 Flash
n'exposent de logprobs via OpenRouter, et aucun modèle n'y expose ceux du prompt. Le mécanisme qui a
produit leurs scores Min-K% pour ces modèles reste à expliquer (question R1 aux auteurs). Le support
a pu changer depuis leurs expériences.

## Alertes

- **Gemini 2.5 Flash est déprécié** : à partir du **1er décembre 2026**, les requêtes vers
  `gemini-2.5-flash` sont **redirigées automatiquement vers `gemini-3.5-flash-lite`** [D5]. Tout résultat
  obtenu après cette date sous ce nom concernerait un autre modèle. Le paramètre `responseLogprobs`
  est aussi annoncé comme déprécié pour Gemini 3.x [D12].
- **GPT-5 est marqué « Deprecated »** sur la page modèle OpenAI [D3].
- **Tendance générale** : les modèles de raisonnement récents retirent les logprobs (OpenAI les
  interdit dès que `reasoning_effort` n'est pas `none` [D1] ; Google les déprécie pour Gemini 3.x [D12]).

## Lecture provisoire (à confirmer par les tests réels)

| Modèle | Scores sur logprobs du prompt (Min-K%...) | Repli possible |
|---|---|---|
| GPT-5 | impossible d'après la doc | méthodes sur texte généré seul (`papers/mia-boite-noire/`) |
| Gemini 2.5 Flash | impossible d'après la doc | logprobs de complétion (Vertex AI) ou texte seul ; modèle bientôt remplacé |
| Mistral Small 24B | possible (local, ou `prompt_logprobs` de l'API Mistral à tester) | |
| LLaMA 3.3 70B | possible (Together `echo`, ou local avec GPU suffisant) | |
| DeepSeek-V3 | pas via l'API officielle ; local très coûteux (671B) | provider tiers avec prompt logprobs à chercher, ou logprobs de complétion |

Décision à prendre et à consigner dans `notes/decisions.md` après les tests réels.

## Tests réels à faire (non faits)

Un appel minimal par voie : prompt d'environ 30 tokens de code, `max_tokens` = 1 à 5.
Coût estimé : moins de 0,001 $ par appel, **moins de 0,01 $ au total** pour les voies ci-dessous.
Pour chaque appel, enregistrer la réponse brute et vérifier la présence effective des logprobs (pas
seulement l'absence d'erreur).

1. OpenAI : `gpt-5` en Chat Completions avec `logprobs: true` (erreur attendue).
2. Gemini : `gemini-2.5-flash` avec `responseLogprobs` sur l'API à clé, puis sur Vertex AI.
3. Mistral : API Mistral avec `prompt_logprobs: true` sur Mistral Small.
4. Together : Llama 3.3 70B en completions avec `echo: true` et `logprobs: 1`.
5. DeepSeek : `deepseek-chat` avec `logprobs: true`.
6. OpenRouter : les 8 IDs ci-dessus avec `logprobs: true` et `require_parameters: true`.

Clés nécessaires (dans `.env`, jamais commitées) : OpenAI, Google (AI Studio et/ou Vertex), Mistral,
Together, DeepSeek, OpenRouter.

## Sources

- [D1] OpenAI, guide « Using the latest model » : « When reasoning effort is not none, remove temperature,
  top_p, and top_logprobs. For Chat Completions, also remove logprobs. » ; la page GPT-5 indique
  « Reasoning.effort supports: minimal, low, medium, and high » (pas `none`).
  https://platform.openai.com/docs/guides/latest-model et https://platform.openai.com/docs/models/gpt-5
- [D2] Le paramètre `echo` (logprobs du prompt) n'existe que sur l'endpoint legacy `/v1/completions`,
  dont les exemples utilisent `gpt-3.5-turbo-instruct`, pas GPT-5.
  https://developers.openai.com/api/reference/resources/completions/methods/create
- [D3] Page modèle GPT-5 (prix, cutoff « Sep 30, 2024 », statut Deprecated). https://platform.openai.com/docs/models/gpt-5
- [D4] Référence API Gemini, `generationConfig.responseLogprobs` / `logprobs` (0 à 20), `logprobsResult`
  « for the response tokens ». https://ai.google.dev/api/generate-content
- [D5] Page modèle Gemini 2.5 Flash (cutoff janvier 2025, dépréciation et redirection au 2026-12-01).
  https://ai.google.dev/gemini-api/docs/models/gemini-2.5-flash
- [D6] Référence API Mistral, chat completions : paramètres `logprobs`, `prompt_logprobs`, `top_prompt_logprobs`
  (sans description détaillée sur la page). https://docs.mistral.ai/api/endpoint/chat
- [D7] Catalogue OpenRouter, `supported_parameters` et `pricing`, relevé le 2026-11-15. https://openrouter.ai/api/v1/models
- [D8] Référence API Together, completions : « When echo is true, the prompt is included in the response.
  Additionally, when logprobs is also provided, log probability information is provided on the prompt. »
  https://docs.together.ai/reference/completions (disponibilité de Llama 3.3 70B en serverless avec echo : à tester)
- [D9] Carte modèle Llama 3.3 : « The pretraining data has a cutoff of December 2023 ».
  https://github.com/meta-llama/llama-models/blob/main/models/llama3_3/MODEL_CARD.md
- [D10] Référence API DeepSeek, create chat completion : `logprobs` « of the output tokens », `top_logprobs` 0 à 20.
  https://api-docs.deepseek.com/api/create-chat-completion
- [D11] OpenRouter, référence des paramètres (`logprobs` : « log probabilities of the output tokens ») et
  vue d'ensemble (paramètres non supportés ignorés). https://openrouter.ai/docs/api-reference/parameters
- [D12] Référence Vertex AI : « The responseLogprobs parameter is deprecated for Gemini 3.x models ».
  https://cloud.google.com/vertex-ai/generative-ai/docs/model-reference/inference
- [F1] Forum Google AI (non officiel) : erreur « Logprobs is not enabled for models/gemini-2.5-flash » sur l'API à clé,
  fonctionne via Vertex AI. https://discuss.ai.google.dev/t/logprobs-is-not-enabled-for-gemini-models/107989
