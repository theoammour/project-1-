# Cryptris - Projet de Cryptographie Gamifiee

Cryptris est un jeu educatif inspire de Tetris, concu pour illustrer les principes de la cryptographie a base de reseaux euclidiens (Lattice-based Cryptography). Le joueur incarne un decodeur qui doit nettoyer des cles publiques "bruitees" pour retrouver le message original.

## Concept du Jeu

Le jeu oppose le Joueur a une IA Espion.
- But du joueur : Vider son plateau en annulant les blocs positifs (bleus) et negatifs (cyans) pour maintenir la hauteur des colonnes a zero.
- Principe mathematique : Chaque piece qui tombe est vecteur d'un reseau. L'objectif est de reduire la norme du vecteur global (la hauteur des colonnes) a zero. C'est une illustration ludique du probleme CVP (Closest Vector Problem).

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
- Traduction : Interface et code entierement traduits en francais.

### Auteur
Ammour Theo (ammour@et.esiea.fr)
