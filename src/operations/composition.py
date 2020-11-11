from homomorphism import Homomorphism

class Composition(Homomorphism):
    """
    f: G -> H
    g: H -> K

    return g◦f: G -> K
    """
    def __init__(self, f : Homomorphism, g : Homomorphism):
        assert(f.codomain() == g.domain())
        self._dom = f.domain()
        self._codom = g.codomain()
        self._f = f
        self._g = g
        self._end = None
        self._iso = None
        self._inj = None
        self._sur = None
    
    def __getitem__(self,k):
        return self._g[self._f[k]]

    def image(self):
        return {self._g(i) for i in self._f.image()}

    def kernel(self):
        return {k for k in self._f.kernel() if self._g(k)==self.codomain().identity()}
