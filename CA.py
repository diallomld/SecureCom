import os
from datetime import datetime, timedelta
from md5 import md5
import rsa as rsa 

chemin_repertoire_script = os.path.dirname(os.path.abspath(__file__))

class CA:
    def __init__(self, nom_):
        self.nom = nom_
        chemin = f'{chemin_repertoire_script}/depot/depot_{self.nom}/' 
        cheminKey = f'{chemin}keys.txt'
        if os.path.exists(chemin + "keys.txt"):
            with open(chemin + "keys.txt") as file:
                contenu = file.read()
                data = contenu.split('\n')
                self.privkey = (int(data[0]), int(data[1]))
                self.pubkey = (int(data[2]), int(data[3]))
        else:
            os.makedirs(chemin)
            p = rsa.generate_prime_number(128)
            q = rsa.generate_prime_number(128)
            self.privkey, self.pubkey = rsa.generate_keypair(p, q)
            fichierKeys = (
                str(self.privkey[0]) + '\n' + str(self.privkey[1]) + '\n' +
                str(self.pubkey[0]) + '\n' + str(self.pubkey[1]) + '\n' +
                str(p) + '\n' + str(q)
            )
            with open(chemin + "keys.txt", 'w') as writer:
                writer.write(fichierKeys)
        
        print("Clé privé du CA : "), print(self.privkey), print("\n" + "########SEPARATION######")
        print("Clé publique du CA : "), print(self.pubkey), print("\n" + "########SEPARATION######")

    def certifGen(self, sujet):
        if sujet == "keys":
            raise ValueError("Non, on ne triche pas")
        chemin = f'{chemin_repertoire_script}/depot/depot_{self.nom}/'
        if not os.path.exists(f'{chemin}/{sujet}.txt'):
            print("CREATION DU CERTIF")
            date = datetime.now()
            certificat = {
                'version': str(3),
                'subject': sujet + "",
                'emmeteur': self.nom + "",
                'validité': {
                    date.strftime("%d:%m:%Y,%H:%M:%S"),
                    (date + timedelta(days=7)).strftime("%d:%m:%Y,%H:%M:%S")
                },
                'public_key:': str(self.pubkey),
            }
            msg = ""
            for valeur in certificat.values():
                msg += str(valeur) + "\n"
            # print("####MSG#####")
            # print(msg)
            # print("MD5 MSG  :  ", str(md5(str(msg))))
            signature = rsa.encrypt(self.privkey, str(md5(str(msg))))
            signatureSTR = ""
            for element in signature:
                signatureSTR += str(element) + '|'
            signatureSTR = signatureSTR[0:-1]
            certif = msg + signatureSTR
            with open(f'{chemin}/{sujet}.txt', 'w') as writer:
                writer.write(certif)
        else:
            with open(f'{chemin}/{sujet}.txt') as file:
                certif = file.read()
        return certif

    def getPubKey(self):
        return self.pubkey


# Vérification du certificat
def verifCert(certificat, CA):
    certifTab = certificat.split("\n")
    msg = ""
    for indice in range(0, 5):
        msg += certifTab[indice] + '\n'
    md = md5(msg)
    keys = CA.getPubKey()
    X = certifTab[4].split(", ")
    x1 = X[0][1:]
    x2 = X[1][0:-1]
    receiveKey = (int(x1), int(x2))
    if keys != receiveKey:
        raise ValueError("Les clés ne correspondent pas")
    else:
        t = str(certifTab[5]).split('|')
        t1 = [int(element) for element in t]
        md5decrypt = rsa.decrypt(keys, t1)
    if md5decrypt == md:
        print("Certificat valide")
        return True
    print("Certificat non valide")
    return False

##  recuperer un certif avec ca et entite
def getCertif(nom_CA, entite):
    chemin = f'{chemin_repertoire_script}/depot/depot_{nom_CA}/'
    
    # Recherche des certificats correspondant au nom de l'entité
    certificats = []
    for filename in os.listdir(chemin):
        if filename.startswith(entite) and filename.endswith(".txt"):
            with open(os.path.join(chemin, filename)) as file:
                certificats.append(file.read())
    
    if certificats:
        return certificats  # Renvoyer la liste des certificats correspondant à l'entité
    else:
        return None  # Renvoyer None si aucun certificat n'a été trouvé pour cette entité

def genarateCertifAndSign():

    # Saisie du nom de l'autorité de certification
    nom = input("Entrer le nom de l'autorite de certif : ")
    ca = CA(nom)
    # Saisie du sujet pour le certificat
    sujet = input("Entrer le nom de l'entité : ")

    # Génération du certificat pour le sujet donné
    certificat = ca.certifGen(sujet)

    print("certificat : ", certificat)

    return (certificat,ca)

def CheckCertif():

    print("################### Vérification du certificat")
    # Saisie du nom de l'autorité de certification
    nom_CA = input("Entrez le nom de l'autorité de certification : ")

    # Saisie du nom de l'entité pour laquelle rechercher le certificat
    entite = input("Entrez le nom de l'entité pour laquelle vous recherchez le certificat : ")

    # Recherche des certificats pour l'entité donnée dans le CA spécifié
    certificats_trouves = getCertif(nom_CA, entite)
    certificat_ = None
    if certificats_trouves is not None:
        print(f"Certificats trouvés pour {entite} emis par {nom_CA}:")
        for certificat in certificats_trouves:
            certificat_ = certificat
            print(certificat)

    else:
        print(f"Aucun certificat trouvé pour {entite} dans {nom_CA}.")

    resultat_verification = verifCert(certificat, CA(nom_CA))
    print("Le certificat est valide :", resultat_verification)
    