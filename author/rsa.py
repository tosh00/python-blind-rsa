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


def invMod(a, b):
    gcd, x, y = egcd(a, b)
    if x < 0:
        x+=b
    return x


def decryptRSAMessage(crypted, e, n):
    return [pow(c, e, n) for c in crypted]

def generateCoprime( number, min = 50, max = 1000):
    res = random.randint(min, max)
    while(math.gcd(res, number) != 1):
        res = random.randint(min, max)
    return res


def shadowing(message, e, n, k):
    return [(m*pow(k, e, n))%n for m in message]

def unshadow(shadowedSignature, e, n, k):
    ik = invMod(k, n)
    return [(sp*ik)%n for sp in shadowedSignature]

def checkSignature(e, n, s, m):
    if(len(s)!=len(m)):
        return False
    for sc, mc in zip(s, m):
        if(pow(sc, e, n)!= mc%n):
            return False
    return True

def generateBlindFactor(n):
    return generateCoprime(n, n>>12, n)

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

def trimDecrypted(b):
    res = []
    flag = False
    for i in b[::-1]:
        if i != 0:
            flag = True
        if flag:
            res.append(i)
    return bytes(res[::-1])