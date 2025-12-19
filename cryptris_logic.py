"""
Cryptris - Logique Mathématique (LWE & Lattice)
Projet ESIEA - Cryptographie Appliquée
Auteur: Théo Ammour
"""
import math
import random
from settings import (
    BOARD_SYMBOLS, REPEAT_GEN_PUBLIC_KEY_LIST, REPEAT_CHIFFRE_MSG_LIST,
    PREGENERATED_PRIVATE_KEYS, AUTHORIZED_LENGTH,
    COLUMN_TYPE_1, COLUMN_TYPE_2, COLUMN_TYPE_3
)

# --- Fonctions Utilitaires ---

def positive_modulo(x1, nbr):
    """
    Modulo positif
    Assure que le résultat soit toujours positif : ((x1 % nbr) + nbr) % nbr
    """
    return ((x1 % nbr) + nbr) % nbr

pm = positive_modulo

def ternary_to_symbol(x1, x2, x3, x4):
    """
    Convertit un groupe de 4 chiffres ternaires en symbole correspondant
    """
    i = pm(x1, 3) + 3 * pm(x2, 3) + 9 * pm(x3, 3) + 27 * pm(x4, 3)
    if 0 <= i < len(BOARD_SYMBOLS):
        return BOARD_SYMBOLS[i]
    return BOARD_SYMBOLS[-1] # Retourne le carré si hors limites

def integer_mod3_to_ternary(x):
    """
    Retourne une valeur ternaire (-1, 0, 1) à partir d'un entier, 
    basé sur son modulo 3.
    """
    y = pm(x, 3)
    if y == 2:
        return -1
    else:
        return y

i3t = integer_mod3_to_ternary

def symbol_to_ternary(s):
    """
    Convertit un symbole en sa représentation ternaire.
    Retourne une liste de 4 chiffres ternaires.
    """
    try:
        i = BOARD_SYMBOLS.index(s)
    except ValueError:
        i = len(BOARD_SYMBOLS) - 1 # Défaut : dernier symbole

    x1 = pm(i, 3)
    i = (i - x1) // 3
    x2 = pm(i, 3)
    i = (i - x2) // 3
    x3 = pm(i, 3)
    i = (i - x3) // 3
    x4 = pm(i, 3)
    
    return [i3t(x1), i3t(x2), i3t(x3), i3t(x4)]

def string_to_ternary(string):
    """
    Convertit une chaîne entière en représentation ternaire.
    Retourne une liste de chiffres ternaires (aplatie).
    """
    ternaries = []
    for char in string:
        ternary = symbol_to_ternary(char)
        ternaries.extend(ternary)
    return ternaries

# --- Opérations Vectorielles ---

def rotate(dim, l, i):
    """
    Effectue une rotation circulaire du vecteur vers la gauche.
    """
    # Normalisation de l'indice i
    i = i % dim
    return l[i:] + l[:i]

def sum_vectors(l1, l2):
    """
    Somme élément par élément de deux vecteurs.
    """
    return [x + y for x, y in zip(l1, l2)]

def mult_vector(a, l1):
    """
    Multiplie chaque élément du vecteur par un scalaire 'a'.
    """
    return [a * x for x in l1]

def l2_norm_sq(v):
    """
    Norme L2 au carré (somme des carrés).
    """
    return sum(x * x for x in v)

def score(public_key):
    """
    Évalue la clé publique pour s'assurer de sa jouabilité (complexité).
    """
    max_pk = max(public_key)
    min_pk = min(public_key)
    t = max(min_pk * min_pk, max_pk * max_pk)
    
    distance = l2_norm_sq(public_key)
    
    if t == 0:
        return 0
    else:
        return distance / t

# --- Génération de Clés ---

def gen_public_key(dim, sk, repet):
    """
    Génère une clé publique à partir d'une clé privée par rotations et combinaisons linéaires.
    """
    # Gestion des entrées dictionnaire (pour les clés complexes)
    private_key_vector = sk
    if isinstance(sk, dict):
        private_key_vector = sk['key']
        
    pk = list(private_key_vector) # Copie
    
    for _ in range(repet):
        k = random.randint(0, dim) # Rotation aléatoire
        r = -1
        if random.randint(0, 1) == 1:
            r = 1
            
        rotated_sk = rotate(dim, private_key_vector, k)
        weighted_rotated_sk = mult_vector(r, rotated_sk)
        pk = sum_vectors(pk, weighted_rotated_sk)
        
    return pk

def gen_public_keys():
    """
    Prépare les clés publiques pour chaque taille de plateau autorisée.
    """
    pk = {}
    for length in AUTHORIZED_LENGTH:
        # HARDCORE MODE: No filtering! We take the first generated key.
        # This replicates the original game's randomness.
        candidate_pk = gen_public_key(length, PREGENERATED_PRIVATE_KEYS[length], REPEAT_GEN_PUBLIC_KEY_LIST[length])
        pk[length] = candidate_pk
    return pk

def gen_random_private_key(length):
    """
    Génère une clé privée LISIBLE et FACILE.
    1. Un Pic Majeur (3 à 5).
    2. Reste initialisé à 0.
    3. Correction itérative pour atteindre Somme = 1 (petites touches de +/- 1).
    """
    vector = [0] * length
    
    # 1. Placer un Pic Majeur (Fixé à 3 pour éviter les boucles paires)
    peak_idx = random.randint(0, length - 1)
    peak_val = 3 # FORCE 3. (Avec 4, on peut bloquer sur des 2. Avec 3, tout est cassable).
    vector[peak_idx] = peak_val
    
    # 2. Correction Itérative (On évite de créer un gros tas secondaire)
    current_sum = peak_val
    
    # Tant que la somme n'est pas 1
    # On ajoute ou retire 1, petit à petit, sur des cases NON-PIC
    while current_sum != 1:
        # Choix d'une case au hasard (hors pic)
        rand_idx = random.randint(0, length - 1)
        if rand_idx == peak_idx:
            continue
            
        if current_sum > 1:
            vector[rand_idx] -= 1
            current_sum -= 1
        else: # current_sum < 1
            vector[rand_idx] += 1
            current_sum += 1
            
    return vector

def get_key_info():
    """
    Génère les structures de données complètes pour les clés (publiques et privées).
    Sépare les composantes positives et négatives pour l'affichage graphique.
    """
    pk = gen_public_keys()
    result = {
        'public_key': {},
        'private_key': {}
    }
    
    for index in AUTHORIZED_LENGTH:
        # Initialisation
        result['public_key'][index] = {
            'key': pk[index],
            'normal_key': [],
            'reverse_key': [],
            'number': []
        }
        
        sub_pk = pk[index]
        
        # GENERATION PROCEDURALE
        # Au lieu d'utiliser PREGENERATED_PRIVATE_KEYS, on génère une nouvelle clé valide.
        sk_vector = gen_random_private_key(index)
        
        result['private_key'][index] = {
            'key': sk_vector,
            'normal_key': [],
            'reverse_key': [],
            'number': []
        }
        
        # Traitement de la Clé Publique
        for val in sub_pk:
            if val > 0:
                result['public_key'][index]['normal_key'].append(COLUMN_TYPE_1)
                result['public_key'][index]['reverse_key'].append(COLUMN_TYPE_2)
                result['public_key'][index]['number'].append(val)
            elif val < 0:
                result['public_key'][index]['normal_key'].append(COLUMN_TYPE_2)
                result['public_key'][index]['reverse_key'].append(COLUMN_TYPE_1)
                result['public_key'][index]['number'].append(-1 * val)
            else:
                result['public_key'][index]['normal_key'].append(COLUMN_TYPE_3)
                result['public_key'][index]['reverse_key'].append(COLUMN_TYPE_3)
                result['public_key'][index]['number'].append(val)
                
        # Traitement de la Clé Privée
        # With procedural generation, sk_vector is always a list.
        private_key_vector = sk_vector
            
        for val in private_key_vector:
            if val > 0:
                result['private_key'][index]['normal_key'].append(COLUMN_TYPE_1)
                result['private_key'][index]['reverse_key'].append(COLUMN_TYPE_2)
                result['private_key'][index]['number'].append(val)
            elif val < 0:
                result['private_key'][index]['normal_key'].append(COLUMN_TYPE_2)
                result['private_key'][index]['reverse_key'].append(COLUMN_TYPE_1)
                result['private_key'][index]['number'].append(-1 * val)
            else:
                result['private_key'][index]['normal_key'].append(COLUMN_TYPE_3)
                result['private_key'][index]['reverse_key'].append(COLUMN_TYPE_3)
                result['private_key'][index]['number'].append(val)
                
    return result

# --- Données du Message ---

def create_a_data_message(crypted_message, current_length):
    """
    Formate le message chiffré pour l'affichage dans le jeu.
    """
    data_message = {
        'message_number': [],
        'message_type': [],
        'plain_message': []
    }
    
    for i in range(current_length):
        val = crypted_message[i]
        data_message['plain_message'].append(val)
        
        if val > 0:
            data_message['message_number'].append(val)
            data_message['message_type'].append(COLUMN_TYPE_1)
        elif val == 0:
            data_message['message_number'].append(val)
            data_message['message_type'].append(COLUMN_TYPE_3)
        else:
            data_message['message_number'].append(val * -1)
            data_message['message_type'].append(COLUMN_TYPE_2)
            
    return data_message

# --- Nouveau Chiffrement Simplifié (3 Blocs) ---

def simple_string_to_ternary(text):
    """
    Convertit une chaîne de caractères en vecteur ternaire [-1, 0, 1].
    Formule : (Index(Lettre) - 1) % 3 - 1
    A=1 -> 0 -> -1
    B=2 -> 1 ->  0
    C=3 -> 2 ->  1
    ...
    """
    vector = []
    text = text.upper()
    for char in text:
        if 'A' <= char <= 'Z':
            idx = ord(char) - ord('A') + 1 # 1-26
            val = (idx - 1) % 3 - 1
            vector.append(val)
        elif char == ' ':
             vector.append(0) # Espace = 0
        else:
            # Autres caractères ignorés ou 0
            vector.append(0)
            
    return vector

def encrypt_simple_message(plain_text, public_key, length):
    """
    Chiffre un message texte court en utilisant l'encodage simplifié.
    Retourne UN SEUL vecteur de taille Length (le puzzle).
    """
    # 1. Conversion
    msg_vector = simple_string_to_ternary(plain_text)
    
    # 2. Fit to Length
    if len(msg_vector) > length:
        msg_vector = msg_vector[:length]
    while len(msg_vector) < length:
        msg_vector.append(0)
        
    # 3. Chiffrement LWE (Simulé)
    encrypted = list(msg_vector)
    
    # Import local éviter circulaire
    from settings import REPEAT_CHIFFRE_MSG_LIST
    # NOTE: rotate, sum_vectors, mult_vector are defined in this file.
    
    repetitions = REPEAT_CHIFFRE_MSG_LIST.get(length, 2)
    
    for _ in range(repetitions):
        k = random.randint(0, length)
        r = random.choice([-1, 1])
        
        pk_rot = rotate(length, public_key, k)
        weighted_pk = mult_vector(r, pk_rot)
        encrypted = sum_vectors(encrypted, weighted_pk)
        
    return encrypted
