import os
import base64
from datetime import datetime
from datetime import timedelta
from md5 import md5
import base64
import rsa as rsa 

chemin_repertoire_script = os.path.dirname(os.path.abspath(__file__))

class CA:
    

    def __init__(self,nom_):
        self.nom=nom_
        chemin= f'{chemin_repertoire_script}/depot/depot_{self.nom}/' 
        cheminKey=f'{chemin}keys.txt'
        if os.path.exists(chemin+"keys.txt"):
            with open(chemin+"keys.txt") as file:
                print("lecture du fichier : "+chemin+"keys.txt")
                contenu=file.read()
                data=contenu.split('\n')
                print("CONTENU : " + str(data))
                self.privkey=(int(data[0]),int(data[1]))
                self.pubkey=(int(data[2]),int(data[3]))
        else:
            os.makedirs(chemin)
            p=rsa.generate_prime_number(128)
            q=rsa.generate_prime_number(128)
            self.privkey, self.pubkey= rsa.generate_keypair(p, q)
            fichierKeys=(str(self.privkey[0])+'\n' + str(self.privkey[1])+'\n' + str(self.pubkey[0])+'\n' + str(self.pubkey[1])+'\n'+str(p)+'\n'+str(q))
            with open(chemin+"keys.txt", 'w' ) as writer:
                writer.write(fichierKeys)        
        
        
        print("Clé privé du CA : "), print(self.privkey),print("\n"+"########SEPARATION######")
        print("Clé publique du CA : "), print(self.pubkey),print("\n"+"########SEPARATION######")
        



    def certifGen(self,sujet):
        if sujet=="keys":
            raise ValueError("non non non on ne triche pas")
        chemin= f'{chemin_repertoire_script}/depot/depot_{self.nom}/'
        if not os.path.exists(f'{chemin}/{sujet}.txt'):
            print("CREATION DU CERTIF")
            date=datetime.now()
            certificat={'version':str(3),
                        'subject':sujet+"",
                        'emmeteur':self.nom+"",
                        'validité':{date.strftime("%d:%m:%Y,%H:%M:%S"),(date+timedelta(days=7)).strftime("%d:%m:%Y,%H:%M:%S")},
                        'public_key:':str(self.pubkey),
                        }
            msg=""
            for valeur in certificat.values():
                msg+=str(valeur)+"\n"
            print("####MSG#####")
            print(msg)
            print("MD5 MSG  :  ",str(md5(str(msg))))
            signature=rsa.encrypt(self.privkey,str(md5(str(msg))))
            signatureSTR=""
            for element in signature : 
                signatureSTR+= str(element)+'|'
            signatureSTR=signatureSTR[0:-1]
    #        print("########SignatureSTR#########")
    #        print(signatureSTR)
    #        print("########Signature#########")
    #        print(signature)
            certif=msg+signatureSTR
    #        print("######CERTIFICAT########")
    #        print(certif)
            with open(f'{chemin}/{sujet}.txt','w') as writer:
                writer.write(certif)
        else:
            with open(f'{chemin}/{sujet}.txt') as file:
                certif=file.read()
                #print("Certif a écrir : ",certif)
                
        return certif

    def getPubKey(self):
        return self.pubkey        
######################### FIN DE CLASS###########################
    
nom1="CA1"
ca=CA("CA1")
certif="zetfgzf"

C=ca.certifGen(certif)

def verifCert(certificat,CA):
    ###séparation des informations
    certifTab=certificat.split("\n")
    msg=""
    for indice in range(0,5) :
        msg+=certifTab[indice]+'\n'
 #    print("##############msg##############")
 #    print(msg)
    ####Calcul du md5 du message clair du certificat
    md=md5(msg)

    ###Décrypte du md5 reçus
    keys=CA.getPubKey()
    X=certifTab[4].split(", ") ###variable temporaire pour mettre en forme le tableau
    x1=X[0][1:]
    x2=X[1][0:-1]
    receiveKey=(int(x1),int(x2)) # int des clé contenue dans le certificat

    if keys!=receiveKey:
 #        print("###receiveKey = ",receiveKey)
 #        print("###keys = ", keys)
        raise ValueError("Les clés ne correspondent pas")
    else:
 #        print("####TEST : ",str(certifTab[5]).split('|'))
        t=str(certifTab[5]).split('|')
        t1=[]
        for element in t :
            t1.append(int(element))
        md5decrypt=rsa.decrypt(keys,t1)
 #       print("### MD5 decrypté : ",md5decrypt)
 #        print("### MD5 calculé  : ", md )
    if md5decrypt==md:
        print("Certificat valide")
        return True
    print("certificat non valide")
    
    return False

#verifCert(C,ca)

def getCertif(entite):
    
    return 0    