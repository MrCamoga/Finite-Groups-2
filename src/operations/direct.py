from groups import Group
from functools import reduce
from sympy import lcm

class Direct(Group):
    """
        two ways to call this class:
            1st: Direct(G1,G2,...,Gn)
            2nd: Direct([G1,G2,...,Gn])    i.e.   Direct([Cyclic(3)]*4)
    """
    def __init__(self, *groups):
        if isinstance(groups[0], list):
            groups = groups[0]
        self.factors = groups
        self.card = reduce(lambda a, b: a*b, [G.card for G in self.factors])
        self.abelian = all(G.isAbelian() for G in self.factors)
        self.cyclic = lcm([G.card for G in self.factors]) == self.card and all(
            G.isCyclic() for G in groups)

    def element(self, k):  # Recursive, returns tuple with elements in G[i]
        l = []
        for G in self.factors:
            l.append(G[k % G.card])
            k //= G.card
        return tuple(l)

    def eindex(self, k):  # Non recursive, returns tuple with indices in G[i]
        l = []
        for G in self.factors:
            l.append(k % G.card)
            k //= G.card
        return tuple(l)

    def index(self, e):  # Recursive, e = tuple with elements in G[i]
        k = 0
        f = 1
        for i in range(len(self.factors)):
            k += self.factors[i].index(e[i])*f
            f *= self.factors[i].card
        return k

    def indexe(self, e):  # Non recursive, e = tuple with indices in G[i]
        k = 0
        f = 1
        for i in range(len(self.factors)):
            k += e[i]*f
            f *= self.factors[i].card
        return k

    def op(self, g1, g2):
        t1 = self.eindex(g1)
        t2 = self.eindex(g2)

        return self.indexe([self.factors[i].op(t1[i], t2[i]) for i in range(len(self.factors))])

    def inverse(self, g):
        t = self.eindex(g)
        tinv = [self.factors[i].inverse(t[i])
                for i in range(len(self.factors))]
        return self.indexe(tinv)

    def order(self, g):
        t = self.eindex(g)
        return lcm([self.factors[i].order(t[i]) for i in range(len(self.factors))])

    def __repr__(self):
        return "Direct(" + ",".join(repr(G) for G in self.factors)+")"
