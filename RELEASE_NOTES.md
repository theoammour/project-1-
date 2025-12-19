# Notes de Version - Historique du Projet Cryptris

Ce document retrace l'intégralité du développement du projet Cryptris sur le dernier mois, de la conception du moteur initial à la livraison finale.

## [v1.0.0] - Version Gold (19 Décembre 2024)
**Focus : Finalisation, Localisation et Documentation**

Cette version est celle présentée pour la soutenance. Elle consolide tout le travail précédent et ajoute les couches de finition nécessaires à un produit complet.
- **Localisation** : Traduction intégrale de l'interface et des textes en Français (FR) et Anglais (EN).
- **Documentation In-Game** : Ajout d'une scène dédiée aux ressources pédagogiques.
- **Support Périphériques** : Finalisation de la navigation à la souris et au clavier dans tous les menus.
- **Logo & Branding** : Intégration du logo ESIEA et nettoyage de l'identité visuelle.
- **Correctifs Critiques** :
  - Résolution du crash "Infinite Loop" lors de la génération de clés denses.
  - Correction de la condition de victoire (toutes les colonnes <= 1).
  - Fix du chevauchement de texte dans la documentation.

## [v0.8.0] - Intelligence Artificielle & Modes de Jeu (Semaine du 12 Décembre)
**Focus : Logique de Jeu (Gameplay Loop) & Adversaire**

L'objectif de cette phase était de rendre le jeu jouable et difficile.
- **IA (Espion)** : Implémentation de l'adversaire utilisant une heuristique gloutonne pour résoudre le problème du CVP (Closest Vector Problem).
- **Mode Arcade** : Liaison complète du flux [Menu -> Config -> Jeu -> Game Over/Win].
- **Chiffrement de Messages** : Ajout de la fonctionnalité permettant de générer un niveau à partir d'un texte utilisateur ("Message Secret").
- **Jauges UI** : Ajout de la jauge de sécurité et des indicateurs de progression.

## [v0.5.0] - Création de Clé & Cryptographie (Semaine du 05 Décembre)
**Focus : Implémentation Mathématique & Outils**

Cette semaine a été dédiée au coeur mathématique du projet et à l'outil de création de clé.
- **Mode "Créer Clé"** : Interface permettant de dessiner sa clé privée (Vecteur dense).
- **Mathématiques** :
  - Implémentation des opérations matricielles modulaires.
  - Génération de la clé publique (Mauvaise base) à partir de la clé privée (Bonne base).
  - Calcul de la "Sécurité" d'une clé basé sur la norme des vecteurs.
- **Sauvegarde** : Système de persistance de la clé générée pour l'utiliser en jeu.

## [v0.1.0] - Moteur Physique & Graphique (Semaine du 28 Novembre)
**Focus : Fondations Techniques & Pygame**

Démarrage du projet, mise en place des bases techniques.
- **Initialisation Pygame** : Création de la fenêtre, boucle de jeu principale à 60 FPS.
- **Système de Gestion de Scènes** : Architecture permettant de changer d'écrans (MenuScene, GameScene).
- **Physique des Blocs** :
  - Grille de jeu.
  - Gestion de la gravité (chute des pièces).
  - Gestion des collisions (empilement).
  - Suppression des paires (Moteur de la règle "Modulos").

---
**Total Développement** : 4 Semaines
**Développeur** : Théo Ammour
