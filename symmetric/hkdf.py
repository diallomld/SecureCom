
import os, sys
from . import key_exchange as sharedKey

current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory by going one level up
parent_dir = os.path.dirname(current_dir)
# Add the parent directory to sys.path
sys.path.append(parent_dir)

import sha256

chemin_repertoire_script = os.path.dirname(os.path.abspath(__file__))

def custom_hmac(key, message):
    block_size = 64  # Taille du bloc pour le padding (en octets)
    ipad = 0x36  # Valeur pour l'inner pad
    opad = 0x5c  # Valeur pour l'outer pad

    # Fonction pour réaliser un padding
    def padding(data):
        return data + b'\x00' * (block_size - len(data))

    # Clé longue pour correspondre à la taille du bloc
    if len(key) > block_size:
        key = sha256.generate_hash(key) # Hash de la clé si elle est trop longue

    key += b'\x00' * (block_size - len(key))  # Remplissage de la clé si elle est trop courte

    # XOR de la clé avec les valeurs pour l'inner et outer pad
    inner = bytes(x ^ ipad for x in key)
    outer = bytes(x ^ opad for x in key)

    # Concaténation et hashage des pads avec le message
    inner_hash = sha256.generate_hash(padding(inner) + message)
    final_hash = sha256.generate_hash(outer + inner_hash)

    return final_hash

def custom_kdf(secret_key, num_keys=5):
    derived_kdf_keys = []


    MESSAGE_CONSTANT = bytes([0x01])
    CHAIN_CONSTANT = bytes([0x02])

    for i in range(num_keys):
        # Génère un nonce en tant que message pour la fonction HMAC
        nonce = os.urandom(32) + bytes([i])

        # Clé dérivée à partir de la clé secrète et du nonce
        key_to_derive = secret_key + nonce + MESSAGE_CONSTANT
        key_to_chain = secret_key + nonce + CHAIN_CONSTANT

        # HMAC pour la dérivation de clé
        derived_key = custom_hmac(key_to_derive, nonce)
        derived_chain = custom_hmac(key_to_chain, nonce)

        derived_kdf_keys.append((derived_key,derived_chain))



    return derived_kdf_keys

#Clé principale à dériver

chemin = os.path.join(chemin_repertoire_script, 'cles_ephemere')  # Utilisez os.path.join pour créer le chemin correct


def getLatestIndexFile():
    # Lire le fichier pour obtenir l'index de la dernière ligne
    if os.path.exists(chemin):
        with open(chemin+'/keys.txt', 'r') as file:
            lignes = file.readlines()
            if lignes:
                return int(lignes[-1].split()[0])
            else:
                return 0



def store_kdf_chain_and_list():
    master_key = sharedKey.getSharedKey()
    num_keys = int(input("Entrer le nombre de message "))
    resultat_kdf = custom_kdf(master_key, num_keys)
    chemin_repertoire_script = os.path.dirname(os.path.abspath(__file__))
    chemin = os.path.join(chemin_repertoire_script, 'cles_ephemere')

    dernier_index = getLatestIndexFile()

    for index, (derived_key, derived_chain) in enumerate(resultat_kdf, start=dernier_index + 1):
        print(f"Iteration {index} - Clé dérivée: {derived_key.hex()}, Clé chaînée: {derived_chain.hex()}")

        if not os.path.exists(chemin):
            os.makedirs(chemin)

        with open(os.path.join(chemin, "keys.txt"), 'a') as writer:
            fichier_keys = (f"{index} {derived_key.hex()} {derived_chain.hex()}\n")
            writer.write(fichier_keys)
