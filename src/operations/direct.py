from groups import Group, Subgroup
from functools import reduce
from sympy import lcm

class Direct(Group):
    """
        two ways to call this class:
            1st: Direct(G1,G2,...,Gn)
            2nd: Direct([G1,G2,...,Gn])    e.g.   Direct([Cyclic(3)]*4)
    """
    def __init__(self, *groups):
        if isinstance(groups[0], list):
            groups = groups[0]
        self.factors = groups
        self.card = reduce(lambda a, b: a*b, [G.card for G in self.factors])
        self.generators = self.__getGenerators()
        self.abelian = all(G.isAbelian() for G in self.factors)
        self.cyclic = lcm([G.card for G in self.factors]) == self.card and all(G.isCyclic() for G in groups)
        self.simple = False if len(groups) > 1 else groups[0].simple
        self.id = self.indexe([G.identity() for G in groups])

    def __getGenerators(self):
        if any(G.generators is None for G in self.factors):
            return
        generators = set()
        for i,G in enumerate(self.factors):
            for g in G.generators:
                e = [0]*len(self.factors)
                e[i] = g
                generators.add(self.indexe(e))
        return generators

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
        for i, G in enumerate(self.factors):
            k += G.index(e[i])*f
            f *= G.card
        return k

    def indexe(self, e):  # Non recursive, e = tuple with indices in G[i]
        k = 0
        f = 1
        for i, G in enumerate(self.factors):
            k += e[i]*f
            f *= G.card
        return k

    def op(self, g1, g2):
        t1 = self.eindex(g1)
        t2 = self.eindex(g2)

        return self.indexe([G.op(t1[i], t2[i]) for i, G in enumerate(self.factors)])

    def exponent(self):
        return lcm(list(G.exponent() for G in self.factors))

    def inverse(self, g):
        t = self.eindex(g)
        return self.indexe([G.inverse(t[i]) for i, G in enumerate(self.factors)])

    def order(self, g):
        t = self.eindex(g)
        return lcm([G.order(t[i]) for i,G in enumerate(self.factors)])

    def derivedSubgroup(self):
        return Direct([Subgroup(G,H = list(G.derivedSubgroup())) for G in self.factors])

    def isSolvable(self):
        return all(G.isSolvable() for G in self.factors)

    def __repr__(self):
        return "Direct(" + ",".join(repr(G) for G in self.factors)+")"
