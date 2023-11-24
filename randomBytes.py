import time as T


def randombyte():
    seed = T.time_ns()
    mult = 5
    inc = 3
    mod = 256
    for i in range(0, 20):
        seed = (seed*mult+inc) % mod
        #print("seed 2", seed)
    return seed


def randombytes(nbbytes):
    result = 0
    for i in range(nbbytes):
        result = (result << 8)+randombyte()
        #print("result: ", result)
    return result

# test de l'algo
#nBits = int(input("entrer le nb de Bits "))
#nbgen =(randombytes(nBits))

#print(nbgen)
