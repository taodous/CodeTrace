# Contrôle qualité avant de déclarer une version finie

Automatique (`build_report.py check`, 0 erreur exigée) :
- [ ] compilation latexmk + biber sans erreur, sans référence ni citation indéfinie
- [ ] aucun `\res` inconnu, aucun nombre en dur dans `07-resultats.tex`
- [ ] aucune citation absente de `refs.bib`
- [ ] aucun tiret cadratin, aucun reste de la template TP
- [ ] avertissements (overfull, figures non référencées, biber) traités ou justifiés

Manuel (relire le PDF, pas seulement les sources) :
- [ ] page de titre : version, date, auteurs, encadrants corrects ; en-tête « CodeTrace • Vn »
- [ ] le résumé et l'abstract décrivent l'état **actuel** et disent la même chose
- [ ] les contributions de l'introduction sont toutes réalisées et vérifiables dans le repo
- [ ] chaque nouvelle source du delta a été intégrée ou son exclusion est justifiée dans le CHANGELOG
- [ ] aucun contenu de la version précédente n'a disparu sans entrée dans le CHANGELOG
- [ ] chaque affirmation chiffrée pointe vers un résultat (`\res`, tableau généré) ou une fiche de lecture
- [ ] les éléments « (web) » des notes sont sans chiffre ou marqués `\averifier`
- [ ] labels membre / non-membre documentés dès que des données existent
- [ ] la baseline aveugle (biais temporel) est présente dès qu'il y a des résultats MIA
- [ ] métriques : AUC-ROC et TPR à 1 % / 5 % de FPR avec IC bootstrap ; tests statistiques nommés
- [ ] figures et tableaux annoncés, commentés, légendes autoportantes
- [ ] annexes A (décisions), B (reproductibilité), C (historique) à jour
- [ ] `\afaire` et `\averifier` restants listés dans le résumé à l'utilisateur
- [ ] `version.json` (`sections_touched`) et `CHANGELOG.md` complets
