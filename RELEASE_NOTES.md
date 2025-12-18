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

## Version 1.7 - Configuration de Clés et Équilibrage

### Nouvelles Fonctionnalités
- **Configuration Avancée** : Ajout d'une étape de configuration dans le mode Arcade permettant de choisir le type de clé (Privée ou Publique) pour le Joueur et pour l'IA (Adversaire).
- **Indicateurs Visuels** : Affichage en jeu du type de clé utilisé (CLE PRIV / CLE PUB) avec un code couleur distinct (Cyan / Rose).

### Améliorations de Gameplay
- **Puzzle Partagé (Fairness)** : Le Joueur et l'Espion (IA) affrontent désormais exactement le même puzzle (message chiffré) pour garantir une équité totale.
- **Support Clé Publique** : Le jeu supporte désormais correctement l'utilisation de clés publiques pour la résolution, avec une génération de puzzle adaptée (plus dense) mais garantie résoluble.
- **Robustesse** : Le système de génération de puzzle a été renforcé pour éviter la création de niveaux triviaux (vides ou déjà résolus), assurant un défi constant même avec des configurations aléatoires.
