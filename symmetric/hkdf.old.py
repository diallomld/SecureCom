import hashlib
import os
import hmac
import secrets
from key_exchange import getSharedKey  # Import de la fonction getSharedKey depuis key_exhange.py

hash_function = hashlib.sha256  # Définition de la fonction de hachage à utiliser

# Génération de sels de 256 bits
salt_256_bits = secrets.token_bytes()


# Fonction de calcul de HMAC
def hmac_digest(key: bytes, data: bytes) -> bytes:
    return hmac.new(key, data, hash_function).digest()


# Fonction d'extraction HKDF
def hkdf_extract(salt: bytes, ikm: bytes) -> bytes:
    if len(salt) == 0:
        salt = bytes([0] * hash_function().digest_size)  # Remplacement du sel vide par des zéros
        print("salt ", salt)
    return hmac_digest(salt, ikm)


# Fonction d'expansion HKDF
def hkdf_expand(prk: bytes, info: bytes, length: int) -> bytes:
    t = b""
    okm = b""
    i = 0
    while len(okm) < length:
        i += 1
        t = hmac_digest(prk, t + info + bytes([i]))
        okm += t
    return okm[:length]


# Fonction HKDF combinant l'extraction et l'expansion
def hkdf(salt: bytes, ikm: bytes, info: bytes, length: int) -> bytes:
    prk = hkdf_extract(salt, ikm)
    return hkdf_expand(prk, info, length)


# Fonction de dérivation de clé de message
def derive_message_key(chain_key: bytes, data: bytes) -> bytes:
    hmac_sha256 = hashlib.sha256()
    hmac_sha256.update(chain_key)
    hmac_sha256.update(data)
    return hmac_sha256.digest()


# Fonction de mise à jour de la clé chaînée
def update_chain_key(chain_key: bytes, data: bytes) -> bytes:
    hmac_sha256 = hashlib.sha256()
    hmac_sha256.update(chain_key)
    hmac_sha256.update(data)
    return hmac_sha256.digest()


# Obtention de la clé partagée(MK) depuis un module externe
sharedKey = getSharedKey()

# Extraction de la clé pseudo-aléatoire via HKDF
prk = hkdf_extract(salt=salt_256_bits, ikm=sharedKey)
hkm_exp = hkdf_expand(prk, os.urandom(32), 32)  # Expansion de la clé dérivée

# Affichage de la longueur et de la représentation hexadécimale de la clé dérivée
print("Longueur en octets hkdf_expand:", len(hkm_exp))
print("hkdf_expand hexadicimal", hkm_exp.hex())

# Dérivation d'une clé via HKDF
derived_key = hkdf(salt_256_bits, sharedKey, os.urandom(32), 32)

# Affichage de la longueur et de la représentation hexadécimale de la nouvelle clé dérivée
print("Clé dérivée: 256 bits, ", len(derived_key), ' octetcs')
print("Clé dérivée hexadicimal ", derived_key.hex())

chain_key = derived_key  # Assignation de la clé dérivée à la clé chaînée

# Calcul de la clé de message avec la donnée 0x01
message_key = derive_message_key(chain_key, bytes([0x01]))
print("Clé de message :", message_key.hex())

# Mise à jour de la clé chaînée avec la donnée 0x02
chain_key = update_chain_key(chain_key, bytes([0x02]))
print("Nouvelle clé chaînée :", chain_key.hex())
