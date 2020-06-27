from groups import Group
from sympy import mod_inverse

class FalseWitness(Group):
    """
    Subgroup of multiplicative group of integers mod n

    We know from FLT that for p prime and x=1,...,p-1    x^(p-1) = 1 (mod p)
    If n is composite and x verifies that equality, we say that x is a false witness for n.

    The set of all false witnesses mod n is a subgroup.
    """
    def __init__(self, n):
        e = [k for k in range(1, n) if pow(k, n-1, n) == 1]
        d = {e[i]: i for i in range(len(e))}
        self.element = lambda k: e[k]
        self.index = lambda k: d[k]
        self.card = len(e)
        self.__n = n
        self.op = lambda g, h: self.index((e[g]*e[h]) % n)
        self.abelian = True
        self.inverse = lambda k: self.index(mod_inverse(e[k], n))

    def __repr__(self):
        return "FalseWitness("+str(self.__n)+")"
