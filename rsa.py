import sys
import random
import math
import base64
import timeit, time
#sys.path.append('../')  # Ajoute le chemin du répertoire parent au chemin de recherche des modules

from md5 import *  # Importe les fonctions depuis le fichier md5 du répertoire parent

from utils import clear_screen, bcolors

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def is_prime(n, k=5):
    if n <= 1 or n == 4:
        return False
    if n <= 3:
        return True
    d = n - 1
    while d % 2 == 0:
        d //= 2
    for _ in range(k):
        if not miller_rabin_test(d, n):
            return False
    return True

def miller_rabin_test(d, n):
    a = random.randint(2, n - 2)
    x = pow(a, d, n)
    if x == 1 or x == n - 1:
        return True
    while d != n - 1:
        x = (x * x) % n
        d *= 2
        if x == 1:
            return False
        if x == n - 1:
            return True
    return False

def generate_prime_number(bits):
    while True:
        num = random.getrandbits(bits)
        if is_prime(num):
            return num

def generate_keypair(p, q):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError("les deux doivent etre premier.")
    if p == q:
        raise ValueError("p et q doivent etre different.")

    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randrange(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    d = mod_inverse(e, phi)

    #print("p q n phi e d",[ p, q, n, phi, g, d])

    return ((e, n), (d, n))

def encrypt(public_key, plaintext):
    e, n = public_key
    cipher = [pow(ord(char), e, n) for char in plaintext]
    return cipher

def decrypt(private_key, ciphertext):
    d, n = private_key
    plain = [chr(pow(char, d, n)) for char in ciphertext]
    return ''.join(plain)

def int_to_bytes(x):

    num_bits = x.bit_length()
    num_bytes = (num_bits + 7) // 8
    
    # print("numbits, numbytes: ", num_bits, num_bytes)
    # Convertir l'entier en une chaîne d'octets
    byte_string = x.to_bytes(num_bytes, byteorder='big')
    
    return byte_string


if __name__ == "__main__":
    
    
    clear_screen()

    COLORS = bcolors()

    bits = int(input(" entrer le nombre de bits de n: "))
    
    start_time1 = time.time()

    # Générer deux nombres premiers aléatoires
    p = generate_prime_number(bits // 2)
    q = generate_prime_number(bits // 2)

    end_time1 = time.time()
    execution_time1 = end_time1 - start_time1

    print(f" {COLORS[0]} Temps d'exécution pour les deux premiers: {round(execution_time1,2)} secondes {COLORS[3]}")

    start_time2 = time.time()

    # Générer la paire de clés
    public_key, private_key = generate_keypair(p, q)

    end_time2 = time.time()
    execution_time2 = end_time2 - start_time2

    print(f"Temps d'exécution pub key et private key: {round(execution_time2,2)} secondes")

    message = input("Entrer le message a crypter: ")

    # Chiffrer le message

    # cipher in base64

    start_time3 = time.time()

    encrypted_msg = encrypt(public_key, message)
    encrypted_bytes = b''.join([int_to_bytes(char) for char in encrypted_msg])
    encrypted_base64 = base64.b64encode(encrypted_bytes).decode('utf-8')
    print("Texte chifré (Base64):", encrypted_base64)
    print("Hash du chifré (md5):", md5(encrypted_base64))

    end_time3 = time.time()
    execution_time3 = end_time3 - start_time3

    print(f"Temps d'exécution pour l'encryption: {round(execution_time3,2)} secondes")
    
    # Déchiffrer le message

    start_time4 = time.time()
    decrypted_msg = decrypt(private_key, encrypted_msg)

    end_time4 = time.time()
    execution_time4 = end_time4 - start_time4

    print(f"Temps d'exécution pour le dechiffrment: {round(execution_time4,2)} secondes")
    print("Texte decrypte:", decrypted_msg)