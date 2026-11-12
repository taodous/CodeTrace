# CodeTrace : Detecting Training Data Provenance in LLMs (code)

Projet de recherche ECE 2026-2027, équipe Data & IA.
Encadrants : Subhankar Maity, Guilherme Medeiros Machado.

## État actuel du projet (à tenir à jour)
Le repo n'est qu'un squelette. Rien n'est implémenté :
- aucun code dans src/ (seulement des `__init__.py` vides), aucun test ;
- aucun dataset dans data/, aucune expérience dans experiments/, aucun résultat dans results/ ;
- aucun papier dans papers/, aucune fiche de lecture dans notes/ ;
- docs/model_access.md et les fichiers de notes sont des gabarits vides.

Ne jamais affirmer qu'un fichier, un résultat ou un papier existe sans l'avoir vérifié dans le repo.
Mettre à jour cette section quand une brique devient réelle.

## Question de recherche
Peut-on déterminer si un extrait de code donné a fait partie des données d'entraînement
d'un LLM, en comparant le comportement du modèle (token log-probabilities, sorties)
sur la version authentique et sur des versions perturbées du même code ?

## Objectifs (du sujet)
1. Curer des datasets de code réels + générer des variantes synthétiques (perturbations).
2. Tester l'appartenance au training set en comparant authentique vs perturbé.
3. Évaluer plusieurs LLMs (le sujet cite GPT-5, Gemini 2.5 Flash, Mistral 24B, LLaMA 3.3 70B, DeepSeek).
4. Définir des critères de décision robustes, par modèle et par type de code.
5. Visualiser et comparer avec des métriques standard.
6. Construire un outil interactif de test en temps réel.
7. Analyser l'influence de l'architecture et des caractéristiques du code.

## Littérature (rien n'est encore lu ni téléchargé)
Pistes de départ, à récupérer dans papers/ et à ficher avec /new-paper avant de s'en servir :
- Shi et al. 2024 (ICLR) : Min-K% Prob, benchmark WikiMIA.
- Zhang et al. 2025 (ICLR) : Min-K%++.
- Duan et al. 2024 : "Do Membership Inference Attacks Work on Large Language Models?"
  (biais de distribution temporelle).
- Un papier de l'équipe encadrante (Maity et al.) sur l'audit d'API LLM via les token probabilities :
  référence exacte à obtenir auprès des encadrants.
Ne pas citer de chiffre ou de conclusion d'un papier tant qu'il n'a pas de fiche dans notes/.

## Règles méthodologiques
- Membres vs non-membres : toujours documenter comment le label est obtenu
  (date de cutoff du modèle, date du commit, dataset public connu comme The Stack).
- Se méfier du biais temporel : un classifieur qui sépare "vieux code" et
  "code récent" sans MIA est une baseline obligatoire.
- Métriques : AUC-ROC, TPR @ 1% et 5% FPR, avec intervalles de confiance (bootstrap).
- Tests statistiques explicites (Wilcoxon / permutation) quand on compare deux méthodes.
- Chaque résultat chiffré du rapport doit pointer vers un fichier dans results/ et une config.
- Seeds fixées, configs versionnées, aucun chiffre recopié à la main.
- Les décisions méthodologiques sont consignées dans notes/decisions.md avec leur justification.

## Contraintes d'accès aux modèles
- Vérifier pour CHAQUE modèle si l'API renvoie les logprobs, et si c'est sur le prompt ou
  seulement sur la complétion. Consigner la réponse (avec source et date) dans docs/model_access.md.
- Point critique à vérifier en premier : les scores type loss / Min-K% / Min-K%++ demandent les
  logprobs des tokens du code fourni en entrée. Les API fermées (OpenAI, Gemini) semblent ne les
  donner que sur les tokens générés ; si c'est confirmé, il faudra une autre méthode pour elles
  (par exemple scorer une complétion du code).
- Modèles open-weights (Mistral, LLaMA, DeepSeek) : accès complet aux logits via
  vLLM / transformers, ou via un provider qui expose les logprobs du prompt.
- Ne jamais commiter de clés API. Elles vivent dans .env (ignoré par git).
- Toujours estimer le coût d'un run API avant de le lancer et le signaler.

## Structure du repo (dossiers créés, vides pour l'instant)
- data/raw, data/processed : datasets, hors git (voir data/README.md)
- src/codetrace/data : collecte, filtrage, déduplication
- src/codetrace/perturb : perturbations de code (renommage, reformatage, réordonnancement, commentaires...)
- src/codetrace/models : wrappers unifiés par modèle, renvoient des logprobs par token
- src/codetrace/attacks : scores MIA (loss/perplexity, zlib, Min-K%, Min-K%++, comparaison perturbée)
- src/codetrace/eval : métriques, bootstrap, tests stats
- tests/ : tests pytest
- experiments/ : configs YAML + scripts de lancement
- results/ : sorties brutes (jsonl) + tableaux agrégés ; les gros fichiers bruts restent hors git
- app/ : outil interactif (Streamlit ou Gradio, à choisir)
- docs/ : documentation technique (model_access.md)
- notes/ : journal, décisions, related work, fiches de lecture
- papers/ : PDF des papiers (hors git, voir .gitignore)
- paper/ : rapport LaTeX

## Conventions de code
- Python 3.11+, uv pour l'environnement (pyproject.toml), ruff + pytest.
- Fonctions pures et testées pour les scores MIA (tests unitaires sur cas jouets).
- Cache disque de toutes les réponses API dans .cache/ (clé = modèle + hash du prompt) :
  on ne paie jamais deux fois.
- Logs d'expériences dans results/<date>_<nom>/ avec la config copiée.

## Comment travailler avec Claude ici
- Pour toute nouvelle expérience : passer d'abord en plan mode, valider le protocole, puis coder.
- Mettre à jour notes/journal.md à la fin de chaque session (/session-end).
- Nouveau papier : /new-paper <chemin PDF ou lien arXiv>.
- Style d'écriture : pas de tirets cadratins dans les textes rédigés.
