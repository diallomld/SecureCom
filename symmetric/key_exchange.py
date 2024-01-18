import os
import random

# Fonction pour générer une clé privée sécurisée de 1024 bits
def generate_private_key():
    private_key_bytes = os.urandom(128)  # 128 octets pour 1024 bits
    private_key = int.from_bytes(private_key_bytes, byteorder='big')
    return private_key

# Fonction pour générer la clé publique à partir de la clé privée
def generate_public_key(private_key, base, prime):
    return pow(base, private_key, prime)

# Fonction pour générer un nombre premier de 1024 bits
def generate_prime():
    while True:
        potential_prime = random.getrandbits(256)
        if potential_prime % 2 != 0 and pow(2, potential_prime - 1, potential_prime) == 1:
            return potential_prime
# pour 1024 its
def find_primitive_root(prime):
    if prime == 2:
        return 1
    p1 = 2
    p2 = (prime - 1) // p1

    while True:
        g = random.randint(2, prime - 1)
        if not pow(g, (prime - 1) // p1, prime) == 1:
            if not pow(g, (prime - 1) // p2, prime) == 1:
                return g



# Génération de clés privées pour Alice et Bob
alice_private_key = generate_private_key()
bob_private_key = generate_private_key()

# Valeurs du groupe (base et nombre premier) - utiliser un nombre premier de 1024 bits
prime = generate_prime()
# Utilisation pour trouver un générateur (élément primitif)
base = find_primitive_root(prime)
#print(f"Générateur trouvé : {base}")

# Génération des clés publiques pour Alice et Bob
alice_public_key = generate_public_key(alice_private_key, base, prime)
bob_public_key = generate_public_key(bob_private_key, base, prime)


alice_public_key_bit = alice_public_key.to_bytes((alice_public_key.bit_length() + 7) // 8, 'big')


#print('alice_public_key ', alice_public_key_bit.hex())

# Échange des clés secrete entre Alice et Bob
shared_secret_alice = pow(bob_public_key, alice_private_key, prime)
shared_secret_bob = pow(alice_public_key, bob_private_key, prime)

# Vérification que les secrets partagés sont les mêmes
assert shared_secret_alice == shared_secret_bob
#print(f"Secret partagé MK : {shared_secret_alice.to_bytes(32, byteorder='big')}")

def getSharedKey():
    return shared_secret_alice.to_bytes(32, byteorder='big')
