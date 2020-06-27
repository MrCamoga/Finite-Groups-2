from groups import Group

class Quotient(Group):
    def __init__(self, G, N):
        assert(G.isNormal(N))
        self.card = G.card//len(N)
        self.cosets = [N]
        self.reprs = [0]
        self.G = G
        self.N = N
        self.abelian = None
        self.cyclic = None

        for i in range(G.card):
            b = True
            for s in self.cosets:
                if i in s:
                    b = False
                    break
            if b:
                self.reprs.append(i)
                self.cosets.append(G.leftcoset(N, i))

        self.index = lambda e: self.cosets.index(e)
        self.element = lambda k: {G.element(i) for i in self.cosets[k]}
        self.op = lambda g, h: self.getCosetIndex(
            G.op(self.reprs[g], self.reprs[h]))

    def inverse(self, g):
        return self.getCosetIndex(self.G.inverse(self.reprs[g]))

    def getCosetIndex(self, g):
        for i in range(len(self.cosets)):
            if g in self.cosets[i]:
                return i
        return -1

    def getCoset(self, g):
        for coset in self.cosets:
            if g in coset:
                return coset
        return None

    def __repr__(self):
        return repr(self.G)+"/"+repr(self.N)

