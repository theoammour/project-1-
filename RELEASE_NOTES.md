# Notes de Version - Projet Cryptris

**Période** : 11 Novembre 2025 - 11 Décembre 2025

Ce document retrace l'historique de développement du projet, réparti sur 4 semaines de travail.

---

## Semaine 1 : Initialisation et Architecture (11 Nov - 17 Nov)

**11 Novembre - Lancement du projet**
*   Initialisation du dépôt Git et structure des dossiers.
*   Analyse du code source original javascript/Sagemath pour comprendre la logique.

**14 Novembre - Configuration**
*   Création du fichier `settings.py`. Définition des constantes globales (couleurs, tailles des blocs, dimensions de l'écran).
*   Création du squelette de `main.py` et mise en place de la boucle principale Pygame.

**17 Novembre - Logique Mathématique (Début)**
*   Implémentation des fonctions de base dans `cryptris_logic.py` (arithmétique modulaire, conversion ternaire).
*   Recherche et intégration des assets graphiques (images de fond, polices).

---

## Semaine 2 : Cœur du Jeu (18 Nov - 24 Nov)

**20 Novembre - Gestion des Vecteurs**
*   Implémentation des opérations vectorielles (somme, multiplication scalaire, rotation) nécessaires pour la cryptographie.
*   Implémentation de la génération des clés (publiques/privées) selon la difficulté choisie.

**22 Novembre - Affichage Statique**
*   Création de la classe `GameBox` dans `game_box.py` pour gérer la zone de jeu.
*   Développement de l'affichage des colonnes de message et de la clé (classe `Column` et sous-classes).

**24 Novembre - Premières Interactions**
*   Implémentation des contrôles clavier (Gauche/Droite pour la rotation).
*   Implémentation de l'inversion de polarité (changement de signe des vecteurs).

---

## Semaine 3 : Dynamique et Règles (25 Nov - 1 Déc)

**27 Novembre - Physique du Jeu**
*   Logique de chute des blocs (gravité) lors de l'application de la clé.
*   Gestion des collisions entre la clé qui tombe et le message.

**29 Novembre - Mécanique d'Annulation**
*   Algorithme complexe d'annulation des blocs (Positif + Négatif = Vide).
*   Gestion des effets visuels lors de la destruction des blocs.

**1 Décembre - Conditions de Jeu**
*   Implémentation des conditions de victoire (message vide) et de défaite (limite de hauteur).
*   Ajout du système de score/timer.

---

## Semaine 4 : Interface, IA et Finalisation (2 Déc - 11 Déc)

**4 Décembre - Intelligence Artificielle**
*   Structure de base de l'IA dans `ai.py`.
*   Intégration de l'IA dans la scène de jeu (écran splitté Joueur vs IA).

**6 Décembre - Menus et Navigation**
*   Création de la scène de Menu Principal et de Configuration (choix difficulté/nom).
*   Gestionnaire de Scènes (`SceneManager`) pour les transitions fluides entre menus et jeu.

**9 Décembre - Polissage**
*   Correction de bugs sur la rotation des clés aux bords du tableau.
*   Ajustement de l'affichage des textes et positionnement des logos partenaires.

**11 Décembre - Finalisation en cours**
*   Nettoyage du code et rédaction du `README.md`.
*   Ajustements divers et polissage.
*   [En cours] Ajout de la saisie de clé privée par l'utilisateur.
*   [En cours] Intégration et affichage du nom de l'utilisateur.

## Semaine 5 : Finalisation et Traduction (12 Déc - 16 Déc)

**14 Décembre - Logique de Jeu Avancée**
*   Séparation des Clés : Le joueur crée une clé personnalisée qui est attribuée à l'espion (IA), tandis que le joueur conserve une clé standard.
*   Validation de la boucle de jeu : Création de clé -> Jeu -> Victoire/Défaite.

**16 Décembre - Polissage Final (En cours)**
*   Traduction intégrale du jeu en Anglais (Internationalisation).
*   Correction de l'affichage de la jauge de sécurité lors de la création de clé.
*   Mise à jour de la documentation.

