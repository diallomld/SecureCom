from utils import clear_screen, bcolors

# import des fichiers

import rsa as rsa
import Guillou as gq
import CA as CA

from blockchain import nft

from symmetric.serpent import serpent
from symmetric.hkdf import store_kdf_chain_and_list



def generer_nombre_premier():
    #return sympy.randprime(100, 1000)

    pass

def chiffrer_dechiffrer_message():
    # Code pour chiffrer / déchiffrer un message
    serpent.menu()

def generer_couple_cle():
    return rsa.generer_couple_cle()

def generer_signer_certificat():
    # Code pour signer un certificat
    CA.genarateCertifAndSign()

def verifier_certificat():
    # Code pour vérifier un certificat
    CA.CheckCertif()

def enregistrer_document_coffre_fort():
    # Code pour enregistrer un document dans le coffre fort
    nft.main()

def envoyer_message_asynchrone():
    # Code pour envoyer un message de manière asynchrone
    store_kdf_chain_and_list()

def demander_preuve_connaissance():
    # Code pour demander une preuve de connaissance
    gq.main()

def main():

    
    while True:
        print("Bonjour ô maître Rémi ! Que souhaitez vous faire aujourd’hui ?")
        print("->1<- Chiffrer / déchiffrer des messages.")
        print("->2<- Créer un couple de clé publique / privée.")
        print("->3<- Signer /Generer un certificat.")
        print("->4<- Vérifier un certificat.")
        print("->5<- Enregistrer un document dans le coffre fort.")
        print("->6<- Envoyer un message (asynchrone).")
        print("->7<- Demander une preuve de connaissance.")
        print("->0<- I WANT IT ALL !! I WANT IT NOW !! SecCom from scratch?")

        choix = input("Veuillez entrer le numéro de votre choix: ")

        if choix == "1":
            chiffrer_dechiffrer_message()
        elif choix == "2":
            generer_couple_cle()
        elif choix == "3":
            generer_signer_certificat()
        elif choix == "4":
            verifier_certificat()
        elif choix == "5":
            enregistrer_document_coffre_fort()
        elif choix == "6":
            envoyer_message_asynchrone()
        elif choix == "7":
            demander_preuve_connaissance()
        elif choix == "0":
            print("I WANT IT ALL !! I WANT IT NOW !! SecCom from scratch?")
            break
        else:
            print("Choix invalide. Veuillez choisir un numéro entre 0 et 7.")

if __name__ == "__main__":
    main()
