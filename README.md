# Cryptris - Projet de Cryptographie Gamifiee

Cryptris est un jeu educatif inspire de Tetris, concu pour illustrer les principes de la cryptographie a base de reseaux euclidiens (Lattice-based Cryptography). Le joueur incarne un decodeur qui doit nettoyer des cles publiques "bruitees" pour retrouver le message original.

## Concept du Jeu

Cryptris est un logiciel pedagogique developpe pour initier aux concepts de la cryptographie asymetrique a base de reseaux. Contrairement a un jeu classique, le but n'est pas simplement de jouer, mais de visualiser le processus de dechiffrement.

- Objectif Pedagogique : Comprendre comment une cle privee (le vecteur que vous controlez) permet de corriger une cle publique bruitee (le plateau rempli) pour retrouver le message original (le plateau vide).
- Mecanique : L'IA agit comme celui qui chiffre le message en ajoutant du "bruit" aleatoire a l'aide de la cle publique. Le joueur agit comme le recepteur legitime qui utilise sa cle privee pour annuler ce bruit et retrouver le secret.
- Mathematiques : C'est une representation visuelle directe du probleme du vecteur le plus proche (CVP) dans un reseau euclidien.

## Installation et Lancement

Pre-requis : Python 3.x et Pygame Community Edition (pygame-ce).

1. Clonez le depot :
   git clone https://gitlab.esiea.fr/ammour/cryptris.git

2. Installez les dependances :
   pip install pygame-ce

3. Lancez le jeu :
   python main.py

## Regles du Jeu

- Deplacement : Fleches Gauche/Droite pour deplacer la cle.
- Action : Fleche Haut ou Espace pour inverser la polarite de la cle (+ / -).
- Validation : Fleche Bas pour appliquer la cle sur le plateau.
- Victoire : Le niveau est gagne lorsque toutes les colonnes ont une hauteur inferieure ou egale a 1 bloc.

## Architecture du Code

- main.py : Point d'entree, gestion des scenes (Menu, Jeu, Victoire) et boucle principale.
- game_box.py : Logique du plateau de jeu, gestion des collisions et conditions de victoire.
- cryptris_logic.py : Coeur mathematique, gestion des vecteurs et generation de cles.
- settings.py : Configuration du jeu, definition des cles et des niveaux de difficulte.
- ai.py : Intelligence Artificielle pour le mode Espion.

## Notes de Version (v1.5)

Cette version apporte des correctifs majeurs pour l'equilibrage et la jouabilite :

### Ameliorations de Gameplay
- Systeme de Cles "Tas de Sable" : Refonte totale des cles pour tous les niveaux. Les "pics" infranchissables ont ete remplaces par une distribution dense de petits blocs. Cela rend le nettoyage du plateau plus fluide et strategique.
- Garantie de Solvabilite : Toutes les cles ont desormais une somme algebrique strictement egale a 1, garantissant mathematiquement qu'il est toujours possible de vider le plateau totalement.

### Corrections de Bugs
- Condition de Victoire : Correction d'un bug ou des colonnes negatives (hauteur -2) etaient considerees comme valides. Le jeu verifie desormais la hauteur absolue des colonnes.
- Boucles Infinies : Resolution definitive des situations de blocage en fin de partie grace au nouveau design des cles.

### Interface
- Popup de Victoire : Nouvelle fenetre de victoire "Challenge Solved" interactive.
- Traduction : Interface et code traduits en francais, anglais et neerlandais.
- Identité Visuelle : Intégration du logo ESIEA.

## Notes de Version (v1.6)

### UI et Internationalisation
- **Langues** : Ajout du support multi-langues (FR, EN, NL) avec selection par drapeaux.
- **Navigation** : Correction de la navigation a la souris dans les menus.
- **Graphismes** : Mise a jour des logos et assets graphiques.

## Notes de Version (v1.7)

### Gameplay et Configuration
- **Configuration des Cles** : Choix independant du type de cle (Privee ou Publique) pour le Joueur et l'adversaire (IA).
- **Equite** : Le Joueur et l'IA partagent desormais le meme puzzle pour garantir une competition equitable.
- **Stabilite** : Amelioration de la generation de niveaux pour eviter les puzzles vides.

### Auteur
Amour Theo (ammour@et.esiea.fr)
