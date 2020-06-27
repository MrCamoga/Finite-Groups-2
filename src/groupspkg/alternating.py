
from math import factorial as fact
from group import Group, composition, functioninverse

class Alternating(Group):
    """
    Alternating group on n letters
    """
    def __init__(self, n):
        self.card = (fact(n)+1)//2
        self.__n = n
        self.element = self.__getperm
        self.index = lambda e: self.__index(e[:])
        self.op = lambda g, h: self.__index(composition(self[h], self[g]))
        self.abelian = n <= 3
        self.cyclic = n <= 3
        self.simple = n >= 5
        self.inverse = lambda k: self.__index(functioninverse(self.element(k)))

    def __repr__(self):
        return "Alternating("+str(self.__n)+")"

    def __getperm(self, k):
        p = []
        f = self.card//self.__n
        arr = [i for i in range(self.__n)]

        even = 0

        for i in range(self.__n-1, 1, -1):
            r = k//f
            p.append(arr.pop(r))
            even += r
            k %= f
            f //= i

        if even % 2 == 0:
            p += arr
        else:
            p += [arr[1], arr[0]]

        return p

    def __index(self, p):
        for i in range(len(p)-2):
            for j in range(i+1, len(p)-2):
                if p[j] > p[i]:
                    p[j] -= 1

        f = self.card//self.__n
        n = 0

        for i in range(len(p)-2):
            n += f*p[i]
            f //= self.__n-1-i
        return n
