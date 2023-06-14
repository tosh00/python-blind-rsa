
from primeGenerator import BigPrimeGenerator
import random
import math


def egcd(a, b):
    s = 0; old_s = 1
    t = 1; old_t = 0
    r = b; old_r = a

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    # return gcd, x, y
    return old_r, old_s, old_t


#modular multiplitive invers of e over fi(N)
#calculate d so that e*d(mod(fi(N))) = 1
def invMod(a, b):
    gcd, x, y = egcd(a, b)
    if x < 0:
        x+=b
    return x


def generateCoprime( number, min = 50, max = 1000):
    res = random.randint(min, max)
    while(math.gcd(res, number) != 1):
        res = random.randint(min, max)
    return res


def generateKeys(length=1000):
    bpg = BigPrimeGenerator()
    p = bpg.generate(length, 60)
    q = bpg.generate(length, 60)
    n = p*q
    totient = (p-1)*(q-1)
    e = generateCoprime(totient, 2>>(length//4), n)
    d = invMod(e, totient)

    return {'private': {'n': n, 'd': d}, 'public': {'n': n, 'e': e}}

def generateSignature(mp, d, n):
    return [pow(c, d, n) for c in mp]

def bytesToInt(src, size):
    p = 0
    res = []
    i = 0
    for b in src:
        p+=b<<8*i
        if (i+1)%size == 0:
            res.append(p)
            p = 0
            i = 0
        else:
            i+=1
    if p != 0:
        res.append(p)
    return res

def intsToBytes(src):
    b = []
    for i in src:
        p = i
        while p != 0:
            b.append(p%2**8)
            p>>=8
    return b

def bytesToInt(src, size):
    p = 0
    res = []
    i = 0
    for b in src:
        p+=b<<8*i
        if (i+1)%size == 0:
            res.append(p)
            p = 0
            i = 0
        else:
            i+=1
    if p != 0:
        res.append(p)
    return res

def intsToBytes(src, size):
    b = []
    for i in src:
        p = i
        for _ in range(size):
            b.append(p%2**8)
            p>>=8
    return bytes(b)

def lengthInBytes(number):
    i=0
    while number != 1:
        i+=1
        number>>=1
    return i