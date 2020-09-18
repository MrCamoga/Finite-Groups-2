from group import composition, functioninverse
from groups import Symmetric, Alternating, Cyclic, Semidirect, Direct, Group, ElementaryAbelianGroup

def GeneralizedSymmetric(m,n):
    """
    The generalized symmetric group is the wreath product Zm≀Sn = (Zm)^n⋊φSn
    with Sn acting on (Zm)^n by φ(σ)(a_1,..., a_n) := (a_σ(1),..., a_σ(n))
    """
    return CompleteMonomialGroup(Cyclic(m),n)

class GeneralizedAlternating(Group):
    """
    The generalized alternating group is the wreath product Zm≀An = (Zm)^n⋊φAn
    with An acting on (Zm)^n by φ(σ)(a_1,..., a_n) := (a_σ(1),..., a_σ(n))
    """
    def __init__(self, m, n):
        A = Alternating(n)
        C = ElementaryAbelianGroup(m,n)

        self.card = A.card*C.card
        self.__dim = (m,n)
        self.index = lambda e: C.index(e[0]) + A.index(e[1])*C.card
        self.element = lambda k: (C[k % C.card], A[k//C.card])
        self.op = lambda k1, k2: C.op(k1 % C.card, C.index(composition(functioninverse(A[k1//C.card]), C[k2 % C.card]))) + A.op(k1//C.card, k2//C.card)*C.card
        self.abelian = None
        self.cyclic = None
        self.simple = None
        self.id = 0

    def isSolvable(self):
        return self.__dim[1] <= 4

    def __repr__(self):
        return "GeneralizedSymmetric"+str(self.__dim)

def CompleteMonomialGroup(G,n):
    D = Direct([G]*n)
    S = Symmetric(n)
    return Semidirect(D, S, lambda s, d: D.indexe(composition(functioninverse(S[s]),D.eindex(d))))

def WreathSymmetric(m,n):
    """
    Sm≀Sn
    """
    return CompleteMonomialGroup(Symmetric(m),n)

class WreathCyclic(Group):
    """
    Cm≀Cn
    """
    def __init__(self,m,n):
        self.__m = m
        self.__n = n
        self.A = ElementaryAbelianGroup(m,n)
        self.B = Cyclic(n)
        self.card = self.A.card*self.B.card
        self.index = lambda e: self.A.index(e[0])+self.B.index(e[1])*self.A.card
        self.element = lambda k: (self.A.element(k % self.A.card), self.A.element(k//self.A.card))
        self.op = lambda a,b: self.A.op(a%self.A.card, sum(divmod(b%self.A.card*self.__m**(a//self.A.card),self.A.card))) + self.B.op(a//self.A.card, b//self.A.card)*self.A.card

        self.abelian = None
        self.cyclic = None
        self.simple = None
        self.id = 0

    def isSolvable(self):
        return True

    def __repr__(self):
        return "WreathCyclic("+str(self.__m)+","+str(self.__n)+")"

def HyperOctahedralGroup(n):
    return WreathSymmetric(2,n)
