from sympy import isprime, mod_inverse, gcd, ntheory, factorint
from groups import Direct, Group

class Cyclic(Group):
    def __init__(self, n):
        self.element = lambda k: k % n
        self.index = self.element
        self.op = lambda g, h: (g+h) % n
        self.generators = {1}
        self.card = n
        self.abelian = True
        self.cyclic = True
        self.simple = isprime(n)
        self.id = 0
        self.inverse = lambda g: -g % n
        self.order = lambda g: self.card//gcd(self.card,g)

    def __repr__(self):
        return "Cyclic("+str(self.card)+")"


class Units(Group):
    """
    Multiplicative group of units modulo n

    This group stores all elements in a list. Units2 class is preferred for big groups
    """
    def __init__(self, n):
        f = factorint(n)
        e = [k for k in range(1, n) if all(k%p!=0 for p in f.keys())]
        d = {e[i]: i for i in range(len(e))}
        self.element = lambda k: e[k]
        self.index = lambda k: d[k]
        self.card = len(e)
        self.__n = n
        self.op = lambda g, h: self.index((e[g]*e[h]) % n)
        self.abelian = True
        self.cyclic = None
        self.simple = None
        self.id = 0
        self.inverse = lambda g: self.index(mod_inverse(e[g], n))

    def __repr__(self):
        return "Units("+str(self.__n)+")"


class Units2(Group):
    """
    Multiplicative group of integers modulo n up to isomorphism
    """
    def __init__(self, n):
        factors = ntheory.factorint(n)
        l = list()

        for k, v in factors.items():
            if k == 2:
                if v == 1:
                    continue
                elif v == 2:
                    l.append(2)
                else:
                    l += [2, 2**(v-2)]
            elif v == 1:
                l.append(k-1)
            else:
                l += [k-1, k**(v-1)]
        l.sort()
        groups = [Cyclic(i) for i in l]
        G = Direct(groups)
        self.element = G.element
        self.index = G.index
        self.card = G.card
        self.__n = n
        self.op = G.op
        self.generators = G.generators
        self.abelian = G.abelian
        self.cyclic = None
        self.simple = None
        self.id = 0

    def __repr__(self):
        return "Units2("+str(self.__n)+")"


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
        self.cyclic = None
        self.simple = None
        self.id = 0
        self.inverse = lambda k: self.index(mod_inverse(e[k], n))

    def __repr__(self):
        return "FalseWitness("+str(self.__n)+")"


def ElementaryAbelianGroup(p,n):
    """
    Elementary Abelian group of order p^n
    """
    assert(isprime(p))
    return Direct([Cyclic(p)]*n)


def KleinGroup():
    return ElementaryAbelianGroup(2,2)

