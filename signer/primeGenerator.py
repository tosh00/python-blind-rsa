import random
import time


class BigPrimeGenerator:
    def __init__(self):
        self.fitst_primes = self.getFirst100primes()

    def getFirst100primes(self):
        res = [2, 3]
        i = 5
        while len(res) < 100:
            if(self.isPrime(i)):
                res.append(i)
            i += 2
        return res

    def isPrime(self, number):
        if number % 2 == 0:
            return False
        for x in range(3, number, 2):
            if number % x == 0:
                return False
        return True

    def getLowLevelPrime(self, size):
        while True:
            candidate = random.randrange(2**(size-1)+1, 2**size-1)
            for d in self.fitst_primes:
                if candidate % d == 0 and d**2 <= candidate:
                    break
                else:
                    return candidate

    def trial(self, number, a, m, k):
        if(pow(a, m, number)) == 1:
            return False
        for i in range(k):
            if(pow(a, (2**i)*m, number)) == number-1:
                return False
        return True

    def millerRabinTest(self, number):
        # number-1 = (2**k) * m
        m = number - 1
        k = 0
        while(m % 2 == 0):
            m >>= 1
            k += 1
        assert(m*(2**k) == number-1)
        i = 0
        for _ in range(self.accuracy):
            i+=1
            a = random.randrange(2, number-1)

            if(self.trial(number, a, m, k)):
                return i
        # print(i)
        return False

    def generate(self, size, accuracy):
        start = time.time()
        self.accuracy = accuracy
        i = 0
        sum = 0
        while(1):
            candidate = self.getLowLevelPrime(size)
            result = self.millerRabinTest(candidate)
            if(not result):

                # try:
                    # writeToFile([i, sum/i, time.time()-start])
                # except:
                    # writeToFile([i, 0, time.time()-start])
                return candidate
            i+=1
            sum+=result

# def writeToFile(values):
#     with open('stats', 'a') as f:
#         l = ''
#         for arg in values:
#             l+=str(arg)+'\t'
#         f.write(l+'\n')
    
# with open('stats', 'w') as f:
#     f.write('')

# bpg = BigPrimeGenerator()
# for i in range(100):
#     bpg.generate(1000, 6)
#     print(i)