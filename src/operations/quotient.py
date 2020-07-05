from groups import Group

class Quotient(Group):
    def __init__(self, G, N):
        assert(G.isNormal(N))
        self.card = G.card//len(N)
        self.indices = {g:0 for g in N}
        self.reprs = [0]
        self.G = G
        self.N = N
        self.abelian = None
        self.cyclic = None
        self.simple = None
        self.id = self.indices[G.identity()]

        for i in G:
            if i not in self.indices:
                coset = G.leftcoset(N, i)
                for g in coset:
                    self.indices[g] = len(self.reprs)
                self.reprs.append(i)

        self.index = lambda e: self.getCosetIndex(e.pop())
        self.element = lambda k: {G[g] for g in self.getCoset(k)}
        self.op = lambda g, h: self.getCosetIndex(G.op(self.reprs[g], self.reprs[h]))

    def inverse(self, g):
        return self.getCosetIndex(self.G.inverse(self.reprs[g]))

    def getCosetIndex(self, g):
        return self.indices[g]

    def getCoset(self, g):
        return self.G.leftcoset(self.N,g)

    def __repr__(self):
        return repr(self.G)+"/"+repr(self.N)