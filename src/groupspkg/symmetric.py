from group import Group, composition, functioninverse
from groups import Inn
from math import factorial as fact

class Symmetric(Group):
    """
    Symmetric group on n letters
    """
    def __init__(self, n):
        self.card = fact(n)
        self.__n = n
        self.element = self.__lehmer
        self.index = lambda e: self.__lehmerinv(e)
        self.op = lambda g, h: self.__lehmerinv(composition(self[h], self[g]))
        self.generators = {1,sum(fact(k) for k in range(1,n))}
        self.abelian = n <= 2
        self.cyclic = n <= 2
        self.simple = n <= 2
        self.id = 0
        self.inverse = lambda k: self.__lehmerinv(functioninverse(self.element(k)))

    def isSolvable(self):
        return self.__n <= 4

    def __repr__(self):
        return "Symmetric("+str(self.__n)+")"

    def center(self):
        if self.__n == 2:
            return {0, 1}
        return {0}

    def Inn(self):
        if self.__n == 2:
            return Inn(super())
        return self

    def Aut(self):
        if self.__n != 6:
            return self
        else:
            #TODO
            pass

    def __lehmerinv(self, p):
        r = list(range(self.__n))
        f = self.card//self.__n
        n = 0
        for x in range(self.__n-1):
            i = r.index(p[x])
            del r[i]
            n += f*i
            f //= self.__n-1-x
        return n

    def __lehmer(self, k):
        p = self.card//self.__n
        arr = list(range(self.__n))
        perm = []
        for i in range(self.__n-1, 0, -1):
            perm.append(arr.pop(k//p))
            k = k % p
            p //= i

        perm += [arr[0]]

        return perm