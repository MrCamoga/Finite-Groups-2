from groups import Group

class Subgroup(Group):
    """
        Define subgroup by generators or by set of elements
    """
    def __init__(self, G, gens = None, H = None):
        if H is None:
            H = self.__genSubgroup(G, gens)
        self.card = len(H)
        d = {H[i]: i for i in range(len(H))}
        self.element = lambda k: G[H[k]]
        self.index = lambda e: d[G.index(e)]
        self.op = lambda a, b: d[G.op(H[a], H[b])]
        self.abelian = None
        self.cyclic = None
        self.simple = None
        self.id = d[G.identity()]
        self.gens = gens
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

    def __repr__(self):
        return "<"+",".join(str(self.G[g]) for g in self.gens)+">"
