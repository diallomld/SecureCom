import random
import rsa as rsa 
import os, sys
chemin_repertoire_script = os.path.dirname(os.path.abspath(__file__))

"""

from keys.txt
14546460005681618880818843673509312180359770802989505622748442201783940642071
63187298830323079515908132318889605549493785198653733268209922062202636293521
8103932425478129090244529458144930551731662063130077715558550182100668645687
63187298830323079515908132318889605549493785198653733268209922062202636293521
315556947864590797836724718109205994803
200240556444466225173351576733481163307

"""
def expo_rapide(base, exp, mod):
    result = 1
    base = base % mod

    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod

        exp = exp // 2
        base = (base * base) % mod

    return result

def pgcd(a,b):
    while b > 0:
        a, b = b, a % b
    return a

def verifPreuve(ca,entite):
    chemin = f'{chemin_repertoire_script}/depot/depot_{ca}/' 
    cheminKey = f'{chemin}keys.txt'
    cheminEntite = f'{chemin}{entite}.txt'
    if os.path.exists(chemin + "keys.txt"):
        with open(cheminKey) as file:
            contenu = file.read()
            data = contenu.split('\n')
            p = int(data[4])
            q = int(data[5])
            x = int(data[0])
            return (p,q,x)
    else:
         print("L'autorité saisi ou l'entité saisi est incorrect")
         sys.exit()


def main():
     
    ca = (input("Entrer le nom de l'entité que vous voulez tester la preuve de connaissance: "))
    entite = (input("Entrer le nom de l'autorité de certif qui a émit le certificat: "))


    values = verifPreuve(ca,entite)


    p = values[0]
    q = values[1]

    N=p*q
    phi = (p - 1) * (q - 1)
    e = random.randrange(1, phi)

    x = values[2]
    X = pow(x,e,N) 

    y = random.randint(1,phi) 
    Y = pow(y,e,N)

    if (pgcd(x,N)>1):
        print("Attention x ne doit pas etre un facteur de N")

    if (pgcd(y,N)>1):
        print("Attention y ne doit pas etre un facteur de N")

    print("MESR genere ces valeurs:")
    print("x(secret)=\t",x)
    print("N=\t\t",N)
    print("X=\t\t",X)

    print("\MESR genere une valeur aleatoire (y):")
    print("y=",y)
    print("\MESR Calcul Y = y^e (mod N) et passe à Remi:")

    print("Y=",Y)

    print("\Remi genere (c) et envoie a MESR:")

    c = random.randint(1,phi) 
    print("c=",c)
    print("\n MESR calcule z = y.x^c (mod N) et envoie à Remi:")

    # Utilisation de l'exponentiation modulaire pour calculer z
    z = (y * expo_rapide(x, c, N)) % N

    print("\nRemi clacul val=z^e (mod N) et (Y* X^c (mod N)) et veirife si ils sont les memes\n")
    val1= expo_rapide(z,e,N) % N
    val2= (Y* expo_rapide(X,c,N)) % N

    print("val1=\t",val1)
    print("val2=\t",val2)

    if (val1==val2):
        print("La preuve de connaissance de Guillou-Quisquater (RSA) est vérifiée avec succès.")
        print(f'{ca} à pu prouvé que c bien lui qui à emis le certificat de {entite}')
    else:
        print("La vérification de la preuve a échoué.")


if __name__ == "__main__":
    main()