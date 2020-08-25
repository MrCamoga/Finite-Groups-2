from groups import Group

class Subgroup(Group):
    """
        Define subgroup by generators or by set of elements
    """
    def __init__(self, G, gens = None, H = None):
        if H is None:
            H = self.__genSubgroup(G, gens)
        self.card = len(H)
        if type(H) == set:
            H = list(H)
        H.sort()
        self._H = H
        d = {H[i]: i for i in range(len(H))}
        self.element = lambda k: G[k]
        self.index = lambda e: d[e]
        self.op = lambda a, b: G.op(a,b)
        self.inverse = G.inverse
        self.abelian = None
        self.cyclic = None
        self.simple = None
        self.id = G.identity()
        self.generators = gens
        self.G = G

    def __genSubgroup(self, G, gens):
        H = [G.identity()]
        S = {G.identity()}
        size = 1

        while True:
            for g in gens:
                for h in H:
                    p = G.op(h, g)
                    if p not in S:
                        H.append(p)
                        S.add(p)
            if size == len(H):
                break
            size = len(H)
        H.sort()
        return H

    def __iter__(self):
        return SubgroupIter(self)

    def __repr__(self):
        if self.generators is not None:
            return "<"+",".join(str(self.G[g]) for g in self.generators)+">"
        else:
            return repr(self._H)

class SubgroupIter():
    def __init__(self, G):
        self.H = G._H
        self.index = 0

    def __next__(self):
        if self.index < len(self.H):
            g = self.H[self.index]
            self.index += 1
            return g
        raise StopIteration()