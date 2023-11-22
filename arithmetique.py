from randomBytes import *
from sys import getsizeof

def fastExp(a, e, mod):
    if e==0:
        return 1
    if e%2==0:
        return (fastExp((a)%mod, e//2, mod)**2)%mod
    else:
        return (a*fastExp((a)%mod,(e-1)//2,mod)**2)%mod

def fastexp(x,e,mod):
    result=1
    while(e>0):
        if e % 2 == 1:
            result = (result*x) % mod
            e = e-1
        if e%2==0:
            x = (x*x) % mod
            e = e//2
    return result

def rabbinMiller(p):
    nbOctet=64
    if p%2==0 :
        print("rabin miller d'un truc pair : faire attention")
        return False


    for i in range(0,20):
        #tirage d'un nombre
        n = randombytes(20)
        while n > p :
            n = randombytes(4)
            print("n = ", n)
            print("p = ", p)
    # n est-il un témoin de Miller ?
        # si p premier (p-1)=d*2^s
        #calcul de s et d
        s=0
        d=p-1
        while d%2==0:
            s+=1
            d=d//2

        x= fastexp(n,d,p)

        if x==1 or x==-1 :
            return False

        for j in range(s-1):
            x=(x*x)%p
            if x== p-1 :
                return False
    return True


def primeGen(nbOctet):
    p=randombytes(nbOctet)|1
    while(not rabbinMiller(p)):
        print("test rabbinmiller sur :",p)
        p=randombytes(nbOctet)
    print("nombre premier trouvé : ",p)
    return p

primeGen(64)

