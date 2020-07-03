from groups import Symmetric, Homomorphism

class GroupAction():
    def __init__(self,G, X, genimg):
        self._S = Symmetric(len(X))
        genimg = {g:self._S.index(f) for g,f in genimg.items()}
        self._f = Homomorphism(G,self._S,genimg)
        self.X = X
        self.G = G

    def __getitem__(self,g):
        return self._S[self._f[g]]

    def op(self,g,x):
        return self._S[self._f[g]][x]

    def orbit(self,x):
        return {self.op(g,x) for g in range(len(self.G))}

    def stabilizer(self,x):
        return {g for g in range(len(self.G)) if self.op(g,x) == x}

    def isTransitive(self):
        return len(self.orbit(0)) == len(self.X)

    def isFaithful(self):
        return self._f.isInjective()
