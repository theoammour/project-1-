import math
import random
from settings import (
    BOARD_SYMBOLS, REPEAT_GEN_PUBLIC_KEY_LIST, REPEAT_CHIFFRE_MSG_LIST,
    PREGENERATED_PRIVATE_KEYS, AUTHORIZED_LENGTH,
    COLUMN_TYPE_1, COLUMN_TYPE_2, COLUMN_TYPE_3
)

# --- Helper Functions ---

def positive_modulo(x1, nbr):
    """
    Positive modulo
    Ensures the result is always positive: ((x1 % nbr) + nbr) % nbr
    """
    return ((x1 % nbr) + nbr) % nbr

pm = positive_modulo

def ternary_to_symbol(x1, x2, x3, x4):
    """
    Convert a group of 4 ternary digits to the matching character
    """
    i = pm(x1, 3) + 3 * pm(x2, 3) + 9 * pm(x3, 3) + 27 * pm(x4, 3)
    if 0 <= i < len(BOARD_SYMBOLS):
        return BOARD_SYMBOLS[i]
    return BOARD_SYMBOLS[-1] # Return the square box if out of range

def integer_mod3_to_ternary(x):
    """
    Return a ternary from an integer, based on its positive modulo 3 value.
    Returns -1, 0, or 1.
    """
    y = pm(x, 3)
    if y == 2:
        return -1
    else:
        return y

i3t = integer_mod3_to_ternary

def symbol_to_ternary(s):
    """
    Convert a symbol to its ternary representation.
    Returns a list of 4 ternary digits.
    """
    try:
        i = BOARD_SYMBOLS.index(s)
    except ValueError:
        i = len(BOARD_SYMBOLS) - 1 # Default to last symbol if not found

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
    Convert a whole string to its ternary representation.
    Returns a list of ternary digits (flattened).
    """
    ternaries = []
    for char in string:
        ternary = symbol_to_ternary(char)
        ternaries.extend(ternary)
    return ternaries

# --- Vector Operations ---

def rotate(dim, l, i):
    """
    "Rotate" columns to the left (i) times.
    """
    # In Python slicing handles this elegantly, but we need to be careful with 'i' being potentially larger than dim or negative
    # The original JS implementation:
    # for (var a = i; a < dim; ++a) new_l.push(l[a]);
    # for (var a = 0; a < i; ++a) new_l.push(l[a]);
    # This implies 'i' is expected to be within [0, dim).
    
    # Normalize i
    i = i % dim
    return l[i:] + l[:i]

def sum_vectors(l1, l2):
    """
    Sum array elements together.
    """
    return [x + y for x, y in zip(l1, l2)]

def mult_vector(a, l1):
    """
    Multiply each array element by 'a'.
    """
    return [a * x for x in l1]

def l2_norm_sq(v):
    """
    Squared L2 norm (sum of squares).
    """
    return sum(x * x for x in v)

def score(public_key):
    """
    Score the public key to ensure it's playable.
    """
    max_pk = max(public_key)
    min_pk = min(public_key)
    t = max(min_pk * min_pk, max_pk * max_pk)
    
    distance = l2_norm_sq(public_key)
    
    if t == 0:
        return 0
    else:
        return distance / t

# --- Key Generation ---

def gen_public_key(dim, sk, repet):
    """
    Generate public key (When not animated).
    """
    pk = list(sk) # Copy
    
    for _ in range(repet):
        k = random.randint(0, dim) # Random rotation amount. Note: JS used random() * (dim+1) floor, so 0 to dim inclusive?
                                   # JS: Math.floor(Math.random() * (dim + 1)) -> 0 to dim.
                                   # rotate function uses 'i' as index. If i=dim, rotate(dim, l, dim) is same as rotate(dim, l, 0).
        r = -1
        if random.randint(0, 1) == 1:
            r = 1
            
        # pk = sum(pk, mult(r, rotate(dim, sk, k)))
        rotated_sk = rotate(dim, sk, k)
        weighted_rotated_sk = mult_vector(r, rotated_sk)
        pk = sum_vectors(pk, weighted_rotated_sk)
        
    return pk

def gen_public_keys():
    """
    Prepare every public keys (one for each board length).
    """
    pk = {}
    for length in AUTHORIZED_LENGTH:
        is_generated = False
        while not is_generated:
            # sks is PREGENERATED_PRIVATE_KEYS
            candidate_pk = gen_public_key(length, PREGENERATED_PRIVATE_KEYS[length], REPEAT_GEN_PUBLIC_KEY_LIST[length])
            if score(candidate_pk) >= 2:
                pk[length] = candidate_pk
                is_generated = True
    return pk

def get_key_info():
    """
    Create public keys and compute key info (for each board length).
    """
    pk = gen_public_keys()
    result = {
        'public_key': {},
        'private_key': {}
    }
    
    for index in AUTHORIZED_LENGTH:
        # Initialize structures
        result['public_key'][index] = {
            'key': pk[index],
            'normal_key': [],
            'reverse_key': [],
            'number': []
        }
        
        sub_pk = pk[index]
        sub_sk = PREGENERATED_PRIVATE_KEYS[index]
        
        result['private_key'][index] = {
            'key': sub_sk,
            'normal_key': [],
            'reverse_key': [],
            'number': []
        }
        
        # Process Public Key
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
                
        # Process Private Key
        for val in sub_sk:
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

# --- Message Data ---

def create_a_data_message(crypted_message, current_length):
    """
    Compute current message data.
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
