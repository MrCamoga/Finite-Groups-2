from groups import Group, GL

class SL(Group):
    def __init__(self, n, k):
        G = GL(n, k).commutatorSubgroup()
        self.__dim = (n,k)
        self.gens = G.generators
        self.abelian = None
        self.cyclic = None
        self.simple = None
        self.id = None

    def __repr__(self):
        return "SL"+repr(self.__dim)