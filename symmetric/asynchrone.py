import os

def initialize_ratchet(initial_key):
    return initial_key

def generate_next_key(current_key):
    new_key = os.urandom(32)  # Clé de 256 bits (32 octets)
    print("new_key int ", new_key)
    return new_key

# Initialisation avec une clé
initial_key = os.urandom(32)  # Clé de départ
current_key = initialize_ratchet(initial_key)

# Utilisation : Générer une nouvelle clé pour un nouveau message
new_message_key = generate_next_key(current_key)
print(f"Nouvelle clé pour un nouveau message : {new_message_key.hex()}")
