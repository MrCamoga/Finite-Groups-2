from functools import reduce
from groups import Group, Cyclic, Direct, Aut2

class GL(Group):
    """
        GL(n,k): Aut((Z/kZ)^n)
    """
    def __init__(self, n, k):
        G = Aut2(Direct([Cyclic(k)]*n))
        assert(G.card == reduce(lambda a, b: a*b, [pow(k, n)-pow(k, i) for i in range(n)]))
        self.card = G.card
        self.__dim = (n, k)
        self.element = G.element
        self.index = G.index
        self.op = G.op
        self.abelian = n == 1
        self.cyclic = None
        self.simple = None
        self.basis = G.gens
        self.field = G.group

    def __repr__(self):
        return "GL"+repr(self.__dim)