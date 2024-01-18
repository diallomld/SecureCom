from . import constants as constants_values 
from . import helper as help_functions
import base64
import os, sys


current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory by going one level up
parent_dir = os.path.dirname(current_dir)
# Add the parent directory to sys.path
sys.path.append(parent_dir)

from utils import bcolors


class serpant:
    def __init__(self,key):
        key = key.encode('hex')
        bitsInKey = help_functions.keyLengthInBitsOf(key)
        rawKey = help_functions.convertToBitstring(help_functions.reverse(key.lower()), bitsInKey)
        self.userKey = help_functions.makeLongKey(rawKey)

    def encrypt(self,block):
        plainText = help_functions.convertToBitstring(help_functions.reverse(block.encode("hex").lower()), 128)
        cipherText = encrypt(plainText, self.userKey)
        return help_functions.reverse(help_functions.bitstring2hexstring(cipherText)).decode('hex')

    def decrypt(self,block):
        cipherText = help_functions.convertToBitstring(help_functions.reverse(block.encode("hex").lower()), 128)
        plainText = decrypt(cipherText, self.userKey)
        return help_functions.reverse(help_functions.bitstring2hexstring(plainText)).decode('hex')

    def get_block_size(self):
        return 16

def encrypt(plainText, userKey):
    """Encrypt the 128-bit bitstring 'plainText' with the 256-bit bitstring
    'userKey', using the normal algorithm, and return a 128-bit ciphertext
    bitstring."""

    K, KHat = help_functions.makeSubkeys(userKey)

    BHat = help_functions.IP(plainText) # BHat_0 at this stage
    for i in range(constants_values.r):
        BHat = help_functions.R(i, BHat, KHat) # Produce BHat_i+1 from BHat_i
    # BHat is now _32 i.e. _r
    C = help_functions.FP(BHat)

    return C

def decrypt(cipherText, userKey):
    """Decrypt the 128-bit bitstring 'cipherText' with the 256-bit
    bitstring 'userKey', using the normal algorithm, and return a 128-bit
    plaintext bitstring."""

    K, KHat = help_functions.makeSubkeys(userKey)

    BHat = help_functions.FPInverse(cipherText) # BHat_r at this stage
    for i in range(constants_values.r-1, -1, -1): # from r-1 down to 0 included
        BHat = help_functions.RInverse(i, BHat, KHat) # Produce BHat_i from BHat_i+1
    # BHat is now _0
    plainText = help_functions.IPInverse(BHat)

    return plainText


def encryptBitslice(plainText, userKey):
    """Encrypt the 128-bit bitstring 'plainText' with the 256-bit bitstring
    'userKey', using the bitslice algorithm, and return a 128-bit ciphertext
    bitstring."""

    K, KHat = help_functions.makeSubkeys(userKey)

    B = plainText # B_0 at this stage
    for i in range(constants_values.r):
        B = help_functions.RBitslice(i, B, K) # Produce B_i+1 from B_i
    # B is now _r

    return B


def decryptBitslice(cipherText, userKey):
    """Decrypt the 128-bit bitstring 'cipherText' with the 256-bit
    bitstring 'userKey', using the bitslice algorithm, and return a 128-bit
    plaintext bitstring."""

    K, KHat = help_functions.makeSubkeys(userKey)

    B = cipherText # B_r at this stage
    for i in range(constants_values.r-1, -1, -1): # from r-1 down to 0 included
        B = help_functions.RBitsliceInverse(i, B, K) # Produce B_i from B_i+1
    # B is now _0
    
    return B

def text_to_bits(text):
    # Convertir le texte en une séquence de bits ASCII
    bit_sequence = ''.join(format(ord(char), '08b') for char in text)

    # Si la longueur est inférieure à 128 bits, ajouter du padding
    if len(bit_sequence) < 128:
        bit_sequence = bit_sequence.ljust(128, '0')  # Remplir avec des zéros

    # Si la longueur est supérieure à 128 bits, tronquer à 128 bits
    if len(bit_sequence) > 128:
        bit_sequence = bit_sequence[:128]

    return bit_sequence


def bits_to_text(bits):
    split_bits = [bits[i:i+8] for i in range(0, len(bits), 8)]

    # Convertir chaque morceau de 8 bits en caractère ASCII
    text = ''.join(chr(int(bit, 2)) for bit in split_bits)
    
    return text

def bits_to_hex(bits):
    # Convertir la séquence de bits en un nombre entier
    int_value = int(bits, 2)

    # Convertir l'entier en représentation hexadécimale
    hex_value = hex(int_value)

    return hex_value

def hex_to_bits(hex_value):
    # Convertir la valeur hexadécimale en un nombre entier
    int_value = int(hex_value, 16)

    # Convertir l'entier en une séquence de bits de longueur fixe (128 bits)
    bits_sequence = format(int_value, '0128b')  # '0128b' indique la longueur de 128 bits

    return bits_sequence

def bits_to_base64(bits):
    # Diviser la séquence de bits en morceaux de 6 bits
    bits = bits.ljust(((len(bits) + 5) // 6) * 6, '0')

    split_bits = [bits[i:i+6] for i in range(0, len(bits), 6)]

    # Convertir chaque morceau de 6 bits en caractère base64
    base64_sequence = ''.join(base64.b64encode(int(bit, 2).to_bytes(1, byteorder='big')).decode().rstrip('=') for bit in split_bits)

    return base64_sequence

def base64_to_bits(base64_string):
    # Décoder la chaîne Base64
    decoded_bytes = base64.b64decode(base64_string)

    # Convertir les octets en une séquence de bits binaire
    binary_string = ''.join(format(byte, '08b') for byte in decoded_bytes)

    return binary_string

def menu():
    while True:
        print("Menu:")
        print("1. Chiffrer")
        print("2. Déchiffrer")
        print("3. Quitter")

        choix = input("Faites votre choix (1, 2 ou 3): ")

        if choix == "1":
            inputUser = input("Entrer le texte à chiffrer: ")
            inputKeysCipher = input("Entrer la clé de chiffrement en Hexadécimal: ")

            inputUserToBits = text_to_bits(inputUser)

            enc = encrypt(inputUserToBits, help_functions.convertToBitstring(inputKeysCipher, 256))

            octets = int(enc, 2).to_bytes((len(enc) + 7) // 8, byteorder='big')

            # Encoder en base64
            base64_encode = base64.b64encode(octets).decode('utf-8')

            COLORS = bcolors()

            print(f" {COLORS[0]} Chiffré en base64: {base64_encode} {COLORS[3]}")

        elif choix == "2":
            cipherbase = input("Entrer le texte chiffré en base64: ")
            inputKeysDecrypt = input("Entrer la clé de déchiffrement en Hexadécimal: ")

            base64_2_bits = base64_to_bits(cipherbase)

            dec = decrypt(base64_2_bits, help_functions.convertToBitstring(inputKeysDecrypt, 256))

            print(f"{COLORS[0]} Déchiffrement réussi avec succès: {bits_to_text(dec)} {COLORS[3]} ")

        elif choix == "3":
            print("Au revoir!")
            break

        else:
            print("Choix non valide. Veuillez entrer 1, 2 ou 3.")
