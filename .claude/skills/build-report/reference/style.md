# Règles de rédaction du rapport

## Ton et argumentation
- Français académique, à la première personne du pluriel (« nous »), phrases courtes.
- Une idée par paragraphe ; première phrase = l'idée, la suite = la justification.
- Distinguer explicitement trois statuts : **fait mesuré** (renvoi à un résultat), **résultat de la
  littérature** (citation), **hypothèse ou intention** (au conditionnel ou « nous prévoyons »).
- Pas de superlatifs non étayés (« très efficace », « révolutionnaire »). Quantifier ou retirer.
- Toute limite connue est dite, de préférence dans « Discussion et limites ».
- Ne jamais présenter comme fait ce qui n'est pas dans le repo (CLAUDE.md).

## Vocabulaire
- Terme anglais en italique à la première occurrence, avec la traduction :
  « inférence d'appartenance (*membership inference attack*, MIA) ». Ensuite l'acronyme seul.
- Acronymes définis à la première utilisation dans le corps (le résumé compte à part).
- Termes fixés : « membre / non-membre », « extrait de code », « version perturbée »,
  « log-probabilité », « taux de vrais positifs (TPR) à 1 % de faux positifs (FPR) »,
  « modèle à poids ouverts (*open-weights*) », « boîte noire ».
- Noms de modèles exacts avec version (« LLaMA 3.3 70B Instruct », pas « LLaMA »).

## Typographie (LaTeX + babel french)
- **Pas de tirets cadratins** (`—`, `---`) : reformuler avec deux-points, parenthèses ou virgules.
  Le tiret demi-cadratin `--` sert uniquement aux intervalles (pages 10--12).
- Guillemets : `"texte"` (csquotes les transforme en « texte »). Ne pas taper « » à la main.
- Ponctuation haute (`: ; ! ?`) : babel insère l'espace insécable, ne pas en ajouter.
- Nombres : `\num{0.62}` (affiche 0,62), pourcentages `\qty{5}{\percent}` ou `5\,\%`,
  intervalles de confiance `\num{0.62} [\num{0.58}~; \num{0.66}]`. Dans Résultats, uniquement via
  `\res{run}{cle}`.
- Références croisées : `\cref{fig:x}` (« figure 3 »), `\Cref` en début de phrase. Jamais
  « la figure ci-dessous ».
- Citations : `\cite{cle}` avant le point, avec espace insécable : `Min-K\%~\cite{shi2024}.`
  Les auteurs dans le texte : « Shi et al.~\cite{shi2024} montrent que... ».
- Pas de code dans le corps du texte, sauf noms courts en `\texttt{}`. Les exemples de
  perturbation sont des figures `listings` courtes (annexe D ou section 05).

## Figures et tableaux
- Chaque figure ou tableau est **annoncé dans le texte** avant son apparition et **commenté**
  (ce qu'on y voit, ce qu'on en conclut).
- Légende autoportante : quoi, sur quelles données, quel modèle, quelle métrique, n, IC.
- Tableaux `booktabs` (`\toprule \midrule \bottomrule`), sans trait vertical, légende au-dessus.
  Nombres alignés, meilleure valeur en gras seulement si le test statistique la sépare.
- Figures vectorielles (PDF) de préférence, légende en dessous, `[htbp]`, largeur relative
  (`\linewidth`). Axes légendés avec unité. Couleurs lisibles en niveaux de gris.
- Toute figure de résultat vient de `results/<run>/figures/` (traçabilité), jamais d'une capture.

## Équations
- Numérotées seulement si on y renvoie (`equation` + `\label{eq:...}`, sinon `equation*`).
- Notations définies une fois (section 03) et réutilisées : $M$ modèle, $x$ extrait,
  $\tilde{x}$ version perturbée, $s(x, M)$ score, $\tau$ seuil.

## Citations de la littérature
- Un chiffre ou une conclusion d'un papier exige une fiche dans `notes/`. Sinon citer le travail
  sans chiffre, ou `\averifier{...}`.
- Préférer la version publiée (conférence) à la prépublication quand la fiche l'indique.
