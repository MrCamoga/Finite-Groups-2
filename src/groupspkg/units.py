from sympy import mod_inverse, gcd
from groups import Group

class Units(Group):
    """
    Multiplicative group of units modulo n

    This group stores all elements in a list. Units2 class is preferred for big groups
    """
    def __init__(self, n):
        e = [k for k in range(1, n) if gcd(k, n) == 1]
        d = {e[i]: i for i in range(len(e))}
        self.element = lambda k: e[k]
        self.index = lambda k: d[k]
# self.index = lambda k: bisect(e,k)-1    slower (nlogn) but doesn't require inverse dictionary d
        self.card = len(e)
        self.__n = n
        self.op = lambda g, h: self.index((e[g]*e[h]) % n)
        self.abelian = True
        self.inverse = lambda g: self.index(mod_inverse(e[g], n))

    def __repr__(self):
        return "Units("+str(self.__n)+")"

