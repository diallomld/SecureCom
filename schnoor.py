
import random
import rsa

"""

from keys.txt
14546460005681618880818843673509312180359770802989505622748442201783940642071
63187298830323079515908132318889605549493785198653733268209922062202636293521
8103932425478129090244529458144930551731662063130077715558550182100668645687
63187298830323079515908132318889605549493785198653733268209922062202636293521
315556947864590797836724718109205994803
200240556444466225173351576733481163307

"""

# # p = rsa.generate_prime_number(128)
# p = 315556947864590797836724718109205994803
# # q = rsa.generate_prime_number(128)
# q = 200240556444466225173351576733481163307

def find_generator(p):
    factors = []
    phi = p - 1
    for i in range(2, p):
        if phi % i == 0 and pow(i, phi, p) == 1:
            factors.append(i)

    for g in range(2, p):
        is_generator = True
        for factor in factors:
            if pow(g, phi // factor, p) == 1:
                is_generator = False
                break
        if is_generator:
            return g

    return None  # Aucun générateur trouvé

p = rsa.generate_prime_number(128)  # Le nombre premier p
alpha = 5  # Générateur alpha
s = 14546460005681618880818843673509312180359770802989505622748442201783940642071

# Calcul de la clé publique
pub = pow(alpha, s, p)

# Message à prouver
message = "Preuve de connaisance veirifié"

# Étape de l'authentification de Schnorr
# Choix aléatoire d'un nonce m
m = random.randint(1, p - 1)

# Calcul de M = alpha^m
M = pow(alpha, m, p)

# Rémi choisit un nonce aléatoire r
r = random.randint(1, p - 1)

# MESR calcule Preuve = m - r * s
preuve = (m - r * s) % (p - 1)

# Vérification de l'authentification
# Calcul de M = alpha^Preuve * pub^r
check = (pow(alpha, preuve, p) * pow(pub, r, p)) % p

if check == M:
    print("L'authentification de Schnorr est vérifiée avec succès : ", message)
else:
    print("L'authentification a échoué.")

