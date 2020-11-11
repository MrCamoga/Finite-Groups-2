class Morphism():
    def __init__(self,G,H,image:list):
        """
            G,H: Group
            image: list (in the future a function) such that f(x) = image[x]
        """
        self._dom = G
        self._codom = H       
        self._end = None
        self._iso = None
        self._inj = None
        self._sur = None
        self._f = image

    def __call__(self,g):
        return self[g]

    def __getitem__(self,g):
        return self._f[g]
    #todo is hom, end, epic, monic,...
    #todo remove duplicated code from Homomorphism
    def isSurjective(self):
        if self._sur != None:
            return self._sur
        if len(self.domain()) < len(self.codomain()):
            self._sur = False
            return False
        self._sur = len(self.domain()) == len(self.codomain())*len(self.kernel()) 
        return self._sur

    def isInjective(self):
        if self._inj != None:
            return self._inj
        if len(self.domain()) > len(self.codomain()):
            self._inj = False
            return False
        self.kernel()
        return self._inj

    def image(self):
        return set(self._f)

    def kernel(self):
        if self._inj:
            return {self._dom.identity()}
        ker = {g for g in self.domain() if self[g] == self._dom.identity()}
        self._inj = len(ker) == 1
        return ker

    def domain(self):
        return self._dom

    def codomain(self):
        return self._codom

    def section(self):
        assert(self.isSurjective())
        return Morphism(self.codomain(),self.domain(), image=[self._f.index(i) for i in range(len(self.codomain()))])

    def inverse(self):
        assert(self.isInjective())
##        return self.__class__(self.codomain(), self.domain(), {self[i]:i for i in self.domain()}) # Crashea si no es sobreyectiva porque no genera el codominio
        return Morphism(self.codomain(), self.domain(), {self[i]:i for i in self.domain()})


class Homomorphism(Morphism):
    def __init__(self,G,H,genimg: dict = None,image:list =None):
        """
            G, H: Group
            genimg: {g:f(g) for g in gens}
        """
        self._dom = G
        self._codom = H       
        self._end = None
        self._iso = None
        self._inj = None
        self._sur = None
        self._f = self.__createFunction(G,H,genimg) if genimg is not None else image
        if not G.isNormal(self.kernel()) or not H.isSubgroup(self.image()):
            raise Exception("Homomorphism is not well defined")
        self.genimg = genimg

    def __call__(self,g):
        return self[g]

    def __createFunction(self,G,H,genimg):
        if not all(G.order(g)%H.order(h) == 0 for g,h in genimg.items()): #TODO
            raise Exception("Homomorphism is not well defined")
        f = [G.identity()]*G.card

        S = {G.identity()}
        size = 1

        for g, i in genimg.items():
            f[g] = i

        while len(S) != G.card:
            for g in genimg.keys():
                for s in list(S):
                    p = G.op(s,g)
                    f[p] = H.op(f[s],f[g])
                    S.add(p)
            if len(S) == size:
                raise Exception("Set of generators do not generate the domain")
            size = len(S)
        return f

    def isEndomorphism(self):
        if self._end != None:
            return self._end
        self._end = repr(self.codomain()) == repr(self.domain())
        return self._end
 
    def isIsomorphism(self):
        if self._iso != None:
            return self._iso
        self._iso = len(self.codomain()) == len(self.domain()) and self.isInjective()
        return self._iso

    def isAutomorphism(self):
        return self.isEndomorphism() and self.isIsomorphism()

    def isSurjective(self):
        if self._sur != None:
            return self._sur
        if len(self.domain()) < len(self.codomain()):
            self._sur = False
            return False
        self._sur = len(self.domain()) == len(self.codomain())*len(self.kernel()) 
        return self._sur

    def isInjective(self):
        if self._inj != None:
            return self._inj
        if len(self.domain()) > len(self.codomain()):
            self._inj = False
            return False
        self.kernel()
        return self._inj
    
    def __getitem__(self,g):
        """
        returns f(g)
        """
        return self._f[g]

    def image(self):
        return set(self._f)

    def kernel(self):
        if self._inj:
            return {self._dom.identity()}
        ker = {g for g in self.domain() if self[g] == self._dom.identity()}
        self._inj = len(ker) == 1
        return ker

    def domain(self):
        return self._dom

    def codomain(self):
        return self._codom

##    def retract(self):
##        assert(self.isInjective())
##        return Morphism(self.codomain(),self.domain(), genimg={})

    def __mul__(self,other):
        """
        f*g = g◦f
        """
        from groups import Composition
        return Composition(self,other)

# def inverse(f ):
#     assert(f.isInjective())
