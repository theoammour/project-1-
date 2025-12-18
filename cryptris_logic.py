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
        is_generated = False
        attempts = 0
        best_pk = None
        best_score = -1
        
        while not is_generated:
            attempts += 1
            # sks correspond aux clés privées pré-générées
            candidate_pk = gen_public_key(length, PREGENERATED_PRIVATE_KEYS[length], REPEAT_GEN_PUBLIC_KEY_LIST[length])
            s = score(candidate_pk)
            
            if s > best_score:
                best_score = s
                best_pk = candidate_pk
            
            if s >= 2:
                pk[length] = candidate_pk
                is_generated = True
            elif attempts > 100:
                # Utilisation de la meilleure clé trouvée après 100 tentatives
                # pour garantir le chargement du jeu.
                pk[length] = best_pk
                is_generated = True
    return pk

def gen_random_private_key(length):
    """
    Génère une clé privée "Unidirectionnelle PARFAITE".
    
    Correction Finale :
    - On force le PIC à l'index 0.
    - Ainsi, quand le joueur clique sur une colonne, c'est CETTE colonne qui reçoit le Pic.
    - Les compensations sont toujours à DROITE (index +2, +3...).
    - Jamais de retour en arrière (wrap-around limité à la fin du tableau).
    
    Structure Fixe : [Pic, 0, -x, -y, 0, ...]
    """
    vector = [0] * length
    
    # 1. Le Pilier (Toujours à l'index 0 pour viser juste)
    peak_val = random.randint(3, 5)
    peak_idx = 0 # FORCE 0. C'est crucial pour l'intuition "Je clique Ici -> J'agis Ici".
    vector[peak_idx] = peak_val
    
    # 2. Distribution (Strictement à Droite)
    needed = 1 - peak_val
    
    # Options de distance positives uniquement
    if length <= 8:
        dist_options = [2, 3] 
    else:
        dist_options = [2, 3, 4]
        
    while needed != 0:
        dist = random.choice(dist_options)
        # On remplit vers la droite
        target_idx = (peak_idx + dist) % length
        
        # Petit garde-fou : Sur un tableau circulaire, faut pas que 'droite' retombe sur 'gauche' trop vite.
        # Mais avec dist 2/3/4 sur length 8+, on est safe.
        
        step = -1
        if vector[target_idx] > -2:
            vector[target_idx] += step
            needed -= step
            
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
