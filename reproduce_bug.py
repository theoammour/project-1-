
import random

def gen_random_private_key_repro(length):
    vector = [0] * length
    
    # 1. Le Pilier
    peak_val = 5 # FORCE 5 to reproduce
    peak_idx = 0
    vector[peak_idx] = peak_val
    
    # 2. Distribution
    needed = 1 - peak_val # -4
    
    # Options de distance positives uniquement (ORIGINAL CODE)
    if length <= 8:
        dist_options = [2, 3] 
    else:
        dist_options = [2, 3, 4]
        
    attempts = 0
    while needed != 0:
        attempts += 1
        if attempts > 1000:
            print(f"FAILED (Infinite Loop detected) for Length {length}, Peak {peak_val}")
            return False
            
        dist = random.choice(dist_options)
        target_idx = (peak_idx + dist) % length
        
        step = -1
        if vector[target_idx] > -1:
            vector[target_idx] += step
            needed -= step
            
    return True

print("Testing Length 8...")
success = gen_random_private_key_repro(8)
if success:
    print("Success!")
