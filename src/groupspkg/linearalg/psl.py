from groups import Group, SL, Inn

class PSL(Group):
    def __init__(self, n, k):
        G = Inn(SL(n, k),iso=1)
        self.card = G.card
        self.__dim = (n, k)
        self.element = G.element
        self.index = G.index
        self.op = G.op
        self.abelian = G.abelian
        self.cyclic = G.cyclic
        self.simple = n > 2 or (k != 2 and k != 3)

    def __repr__(self):
        return "PSL"+str(self.__dim)
