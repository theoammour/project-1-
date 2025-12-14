import random

# Cryptris configuration file
# Ported from js/cryptris-settings.js

# App URL
APP_URL = "http://inriamecsci.github.io/cryptris"

# Animation settings
ANIMATE_TEXT_DELAY_BETWEEN_LETTERS = 20
READING_DELAY = 4000

# Board Symbols
# 1 character is coded with 4 ternary symbols (3^4 = 81 possibilities)
BOARD_SYMBOLS = [
    " ", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
    ";", ".", ",", "!", "?", "&", "#", "'", "\\", "\"", "(", ")", "+", "-", "*", "/", "|", "□"
]

SOCIAL_ENCRYPTED_MESSAGE_MAX_LENGTH = 140

# Cryptography settings

# How many times should the private key be applied in order to generate a public key
REPEAT_GEN_PUBLIC_KEY_LIST = {
    8: 3,
    10: 7,
    12: 8,
    14: 9,
    16: 10
}

# How many times should the public key be applied to encrypt a message
REPEAT_CHIFFRE_MSG_LIST = {
    8: 7,
    10: 8,
    12: 9,
    14: 10,
    16: 11
}

# AI settings
AI_RANDOM_MOVES_BEFORE_STARTING_CRACKING_ALGORITHM = {
    8: 90,
    10: 250,
    12: 500,
    14: 600,
    16: 700
}

AI_SLOWDOWN = 1

# Random helper
def shuffle_list(lst):
    l = list(lst)
    random.shuffle(l)
    return l

# Board Lengths
MIN_BOARD_LENGTH = 8
MEDIUM_BOARD_LENGTH = 10
MAX_BOARD_LENGTH = 12
SUPER_MAX_BOARD_LENGTH = 14
MEGA_MAX_BOARD_LENGTH = 16

# Private keys
PREGENERATED_PRIVATE_KEYS = {
    # Clés Privées Prégénérées
    # Ces clés sont conçues pour assurer un équilibre entre esthétique (densité visuelle)
    # et jouabilité (somme algébrique égale à 1 pour garantir la solvabilité).
    #
    # Logique "Tas de Sable" : 
    # - Amplitude faible (max 2 ou 3) pour un nivellement fluide.
    # - Haute densité (plusieurs blocs) pour la richesse visuelle.
    # - Espacement pour permettre une précision de jeu.
    
    # Niveau 8 : [2, 1, -1, -1]. Somme=1. 4 blocs actifs.
    8: [2, 0, 1, 0, -1, 0, -1, 0],

    # Niveau 10 : [2, 1, 1, -1, -1, -1]. Somme=1. 6 blocs actifs.
    10: [0, 2, 0, 1, 1, 0, -1, 0, -1, -1],

    # Niveau 12 : [3, 1, -1, -1, -1]. Somme=1. 5 blocs actifs.
    12: [3, 0, 1, 0, -1, 0, -1, 0, -1, 0, 0, 0],

    # Niveau 14 : [2, 1, 1, -1, -1, -1]. Somme=1. 6 blocs actifs.
    14: [2, 0, 1, 0, 1, 0, -1, 0, -1, 0, -1, 0, 0, 0],
    
    # Niveau 16 : [3, 1, 1, -1, -1, -1, -1]. Somme=1. 7 blocs actifs.
    16: [3, 0, 1, 0, 1, 0, -1, 0, -1, 0, -1, 0, -1, 0, 0, 0]
}

AUTHORIZED_LENGTH = [
    MIN_BOARD_LENGTH,
    MEDIUM_BOARD_LENGTH,
    MAX_BOARD_LENGTH,
    SUPER_MAX_BOARD_LENGTH,
    MEGA_MAX_BOARD_LENGTH
]

# Column Types (from game.js logic, inferred)
COLUMN_TYPE_1 = "type1" # > 0 (Blue in player mode)
COLUMN_TYPE_2 = "type2" # < 0 (Dark Blue/Cyan in player mode)
COLUMN_TYPE_3 = "empty"    # == 0

# Visual Settings (Ported from global.js)

# Player Board Colors (Blue Theme)
PLAYER_BOARD_COLORS = {
    'colorLeft': {'type1': (107, 141, 167), 'type2': (20, 115, 158), 'empty': None},
    'colorRight': {'type1': (53, 120, 157), 'type2': (1, 76, 131), 'empty': None},
    'strokeColor': {'type1': (178, 190, 201), 'type2': (0, 143, 148), 'empty': None},
    'numberColor': (0, 231, 112), # #00e770
    'columnColor': (0, 113, 187, 51), # rgba(0, 113, 187, 0.2)
}

# IA Board Colors (Purple Theme)
IA_BOARD_COLORS = {
    'colorLeft': {'type2': (103, 70, 116), 'type1': (116, 109, 116), 'empty': None},
    'colorRight': {'type2': (82, 34, 103), 'type1': (88, 83, 119), 'empty': None},
    'strokeColor': {'type2': (125, 75, 142), 'type1': (189, 187, 191), 'empty': None},
    'numberColor': (211, 0, 136), # #d30088
    'columnColor': (187, 53, 0, 51), # rgba(187, 53, 0, 0.2)
}

# Dimensions
SQUARE_WIDTH = 40
SQUARE_HEIGHT = 30
SPACE_HEIGHT = 4
SPACE_WIDTH = 4
BORDER_WIDTH = 8
BORDER_HEIGHT = 8
COLUMN_WIDTH = SQUARE_WIDTH + 3
