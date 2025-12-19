# Cryptris - Version Python ESIEA

![Logo ESIEA](https://lexpress-education.com/wp-content/uploads/2024/08/ESIEA-320x320.jpg)

## Description
Ce projet est une réimplémentation complète en Python (Pygame) du jeu éducatif **Cryptris**, initialement conçu par l'Inria pour vulgariser la cryptographie à base de **Réseaux Euclidiens** (Lattice-based cryptography).

Le joueur incarne un administrateur système qui doit nettoyer des données bruitées (déchiffrement) à l'aide de sa clé privée, tout en affrontant une IA (Espion) qui tente de casser le code.

## Fonctionnalités Clés
- **Gameplay Asymétrique** : Jouez en défense (Déchiffrement) contre une IA en attaque.
- **Création de Clé Interactive** : Construisez votre propre clé privée en empilant des vecteurs.
- **Chiffrement de Message (Nouveau)** : Saisissez un texte secret ("ESIEA") qui sera converti en énigme mathématique jouable.
- **Internationalisation** : Disponible en Français, Anglais et Néerlandais.
- **Interface Moderne** : Menu intuitif, jauge de sécurité, et effets visuels.

## Installation et Lancement
1. **Prérequis** : Python 3.8+ installé.
2. **Installation des dépendances** :
   ```bash
   pip install pygame numpy
   ```
3. **Lancement** :
   ```bash
   python main.py
   ```

## Structure du Projet
- `main.py` : Point d'entrée, gestion des scènes et boucle de jeu.
- `cryptris_logic.py` : Cœur mathématique (Algorithmes LWE, calculs vectoriels).
- `game_box.py` : Moteur physique du plateau (colonnes, collisions).
- `ai.py` : Intelligence Artificielle (Heuristiques de résolution).
- `rapport.tex` : Rapport académique complet du projet (LaTeX).

## Auteur
**Théo Ammour** - ESIEA (M1 Cybersécurité)
*Projet réalisé dans le cadre du module de Cryptographie Appliquée.*

---
*Ce projet est inspiré du jeu original Cryptris (Inria/CNRS).*
