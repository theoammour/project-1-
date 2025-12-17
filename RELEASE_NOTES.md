# Notes de Version

## Version 1.6 - Mise à jour UI et Internationalisation

### Nouvelles Fonctionnalités
- **Sélection de Langue** : Ajout d'un système de sélection de langue directement depuis le menu principal via des drapeaux cliquables. Langues supportées :
  - Français (FR)
  - Anglais (EN)
  - Néerlandais (NL)
- **Asset Graphique** : Remplacement du logo "Digital Cuisine" par le logo ESIEA dans l'interface.

### Correctifs
- **Navigation Souris** : Correction d'un bug critique empêchant la navigation dans les menus avec la souris.
- **Chargement d'Assets** : Amélioration de la robustesse du chargement des images. Le jeu se lance désormais avec des éléments de secours (fallbacks) si certains fichiers graphiques sont manquants ou corrompus.

### Technique
- Refactoring du `MenuScene` pour inclure un `LanguageManager`.
- Mise à jour des scripts de téléchargement d'assets pour inclure les headers User-Agent nécessaires.
