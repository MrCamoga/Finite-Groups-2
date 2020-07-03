from groups import Group, GL, Inn

class PGL(Group):
    def __init__(self, n, k):
        G = Inn(GL(n,k),iso=1)
        self.card = G.card
        self.__dim = (n, k)
        self.element = G.element
        self.index = G.index
        self.op = G.op
        self.abelian = G.abelian
        self.cyclic = G.cyclic
        self.simple = G.simple

    def __repr__(self):
        return "PGL"+repr(self.__dim)