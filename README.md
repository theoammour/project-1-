# Cryptris - Version Python ESIEA

![Logo ESIEA](https://lexpress-education.com/wp-content/uploads/2024/08/ESIEA-320x320.jpg)

## Description
**Cryptris Python** est une réimplémentation complète et éducative du jeu *Cryptris* (initialement développé par Inria/CNRS) pour illustrer les principes de la **cryptographie asymétrique à base de réseaux euclidiens** (Lattice-based cryptography).

Ce projet a été réalisé en **Python (Pygame)** dans le cadre du module de Cryptographie Appliquée à l'ESIEA. Il vise à vulgariser des concepts complexes comme le problème du vecteur le plus court (SVP) et le problème du vecteur le plus proche (CVP) à travers une mécanique de jeu intuitive type "Tetris".

## Fonctionnalités Principales
- **Mode Arcade (Solo vs IA)** : Affrontez une Intelligence Artificielle qui joue le rôle de l'attaquant (Espion). Vous devez nettoyer le bruit ajouté par l'IA en utilisant votre clé privée.
- **Atelier de Clés (Key Creation)** : Un éditeur visuel permettant de comprendre et de construire sa propre clé privée et de visualiser la "bonne base" vs la "mauvaise base" publique.
- **Chiffrement de Messages** : Une fonctionnalité unique permettant de saisir un texte (ex: "SECRET") qui est ensuite chiffré mathématiquement pour générer le niveau de jeu.
- **Interface Riche** : Menus animés, support souris/clavier complet, et jauge de sécurité dynamique.
- **Localisation** : Interface entièrement traduite en **Français** et Anglais.

## Comment Jouer ?

### Objectif
Le but est d'éliminer tous les blocs présents à l'écran. Chaque colonne d'allumettes représente un vecteur. En les empilant ou les retirant, vous effectuez des additions vectorielles modulo $q$.
- **Victoire** : Toutes les colonnes sont vides ou ont une hauteur de 0/1.
- **Défaite** : Une colonne déborde de l'écran (Trop de bruit).

### Contrôles
| Action | Clavier | Souris |
| :--- | :--- | :--- |
| **Sélectionner Colonne** | `Flèches Gauche / Droite` | `Survol` |
| **Déplacer Bloc** | `Flèches Haut / Bas` | `Clic Gauche` (Déposer) |
| **Valider / Confirmer** | `Entrée` | `Clic sur Bouton` |
| **Retour / Quitter** | `Échap` (Esc) | `Clic sur Retour` |

## Installation

1. **Cloner le projet** ou télécharger les sources.
2. **Prérequis** : Avoir Python 3.8 ou plus récent installé.
3. **Installer les dépendances** :
   ```bash
   pip install pygame numpy
   ```
4. **Lancer le jeu** :
   ```bash
   python main.py
   ```

## Architecture Technique
Le projet suit une architecture modulaire pour séparer la logique mathématique du rendu graphique :
- **`main.py`** : Gestionnaire de scènes (Scene Manager) et boucle principale.
- **`cryptris_logic.py`** : Cœur algorihmique (Génération de clés, LLL, Opérations matricielles).
- **`game_box.py`** : Gestion de la physique et de l'état du plateau de jeu.
- **`ai.py`** : Logique de l'IA adverse (Espion).

## Crédits & Contexte
**Développeur** : Théo Ammour (M1 Cybersécurité - ESIEA)
**Projet Académique** : Ce développement a été réalisé de manière individuelle pour la validation du semestre, inspiré par les travaux de l'équipe Inria sur le jeu original Cryptris.

> *Note : Certains commits historiques peuvent faire référence à une structure d'équipe initiale, mais la réalisation finale est l'œuvre d'un développeur unique.*

---
*Basé sur le jeu original Cryptris (Inria).*
