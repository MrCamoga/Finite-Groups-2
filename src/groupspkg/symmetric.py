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
        self.index = lambda e: self.__lehmerinv(e[:])
        self.op = lambda g, h: self.__lehmerinv(composition(self[h], self[g]))
##        self.generators = {self.__lehmerinv([k for k in range(n-2)]+[n-1,n-2]),self.__lehmerinv([k%n for k in range(1,n+1)])}
        self.abelian = n <= 2
        self.cyclic = n <= 2
        self.simple = n <= 2
        self.inverse = lambda k: self.__lehmerinv(functioninverse(self.element(k)))

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
        for i in range(self.__n):
            for j in range(i+1, self.__n):
                if p[j] > p[i]:
                    p[j] -= 1

        f = self.card//self.__n
        n = 0

        for i in range(0, self.__n-1):
            n += f*p[i]
            f //= self.__n-1-i
        return n

    def __lehmer(self, k):
        p = self.card//self.__n
        arr = [k for k in range(self.__n)]
        perm = []
        for i in range(self.__n-1, 0, -1):
            perm.append(arr.pop(k//p))
            k = k % p
            p //= i

        perm += [arr[0]]

        return perm