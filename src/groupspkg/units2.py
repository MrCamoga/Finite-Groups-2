from sympy import ntheory
from groups import Cyclic, Direct, Group

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
        print([G.card for G in groups])
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

    def __repr__(self):
        return "Units2("+str(self.__n)+")"

