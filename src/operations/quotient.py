from groups import Group

class Quotient(Group):

    def __init__(self, G, N):
        if isinstance(G,Quotient):
            N = set().union(*(G.eindex(k) for k in N))
            G = G.G
        
        assert(G.isNormal(N))
        self.card = G.card//len(N)
        self.indices = {g:0 for g in N}     # natural projection G -> G/N
        self.reprs = [0]
        self.G = G
        self.N = N
        self.abelian = None
        self.cyclic = None
        self.simple = None
        self.id = 0

        for i in G:
            if i not in self.indices:
                coset = G.leftcoset(N, i)
                for g in coset:
                    self.indices[g] = len(self.reprs)
                self.reprs.append(i)

        self.index = lambda e: self.getCosetIndex(e.pop())
        self.eindex = lambda k: frozenset(g for g in self.getCoset(k))
        self.element = lambda k: frozenset(G[g] for g in self.getCoset(k))
        self.op = lambda g, h: self.getCosetIndex(G.op(self.reprs[g], self.reprs[h]))
        self.generators = self.__genGenerators()

    def __genGenerators(self):
        if self.G.generators is None:
            return
        gens = set()
        for g in self.G.generators:
            if g in self.N:
                continue
            b = True
            for h in gens:
                if self.G.op(g,self.G.inverse(self.reprs[h])) in self.N:
                    b = False
            if b:
                gens.add(self.getCosetIndex(g))
        return sorted(list(gens))

    def inverse(self, g):
        return self.getCosetIndex(self.G.inverse(self.reprs[g]))

    def getCosetIndex(self, g):
        return self.indices[g]

    def getCoset(self, g):
        return self.G.leftcoset(self.N,self.reprs[g])

    def __repr__(self):
        return repr(self.G)+"/"+repr(self.N)
