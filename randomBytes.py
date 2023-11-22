import time as T


def randombyte():
    #print("generation d'un byte")
    seed = T.time_ns()
    mult = 5
    inc = 3
    mod = 256
    for i in range(0, 20):
        seed = (seed*mult+inc) % mod
    return seed


def randombytes(nbbytes):
    result = 0
    for i in range(nbbytes):
        result = (result << 8)+randombyte()
    return result

