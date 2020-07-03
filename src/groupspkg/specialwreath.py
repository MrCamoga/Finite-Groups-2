from group import composition
from groups import Symmetric, Alternating, Cyclic, Direct, Group, ElementaryAbelianGroup

class GeneralizedSymmetric(Group):
    """
    The generalized symmetric group is the wreath product Zm≀Sn = (Zm)^n⋊φSn
    with Sn acting on (Zm)^n by φ(σ)(a_1,..., a_n) := (a_σ(1),..., a_σ(n))
    """
    def __init__(self, m, n):
        S = Symmetric(n)
        C = Direct([Cyclic(m)]*n)

        self.card = S.card*C.card
        self.__dim = (m,n)
        self.index = lambda e: C.index(e[0]) + S.index(e[1])*C.card
        self.element = lambda k: (C[k % C.card], S[k//C.card])
        self.op = lambda k1, k2: C.op(k1 % C.card, C.index(composition(S[k1//C.card], C[k2 % C.card]))) + S.op(k1//C.card, k2//C.card)*C.card
        self.abelian = None
        self.cyclic = None

    def __repr__(self):
        return "GeneralizedSymmetric"+str(self.__dim)
    
class GeneralizedAlternating(Group):
    """
    The generalized alternating group is the wreath product Zm≀An = (Zm)^n⋊φAn
    with An acting on (Zm)^n by φ(σ)(a_1,..., a_n) := (a_σ(1),..., a_σ(n))
    """
    def __init__(self, m, n):
        S = Alternating(n)
        C = Direct([Cyclic(m)]*n)

        self.card = S.card*C.card
        self.__dim = (m,n)
        self.index = lambda e: C.index(e[0]) + S.index(e[1])*C.card
        self.element = lambda k: (C[k % C.card], S[k//C.card])
        self.op = lambda k1, k2: C.op(k1 % C.card, C.index(composition(S[k1//C.card], C[k2 % C.card]))) + S.op(k1//C.card, k2//C.card)*C.card
        self.abelian = None
        self.cyclic = None

    def __repr__(self):
        return "GeneralizedSymmetric"+str(self.__dim)

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

    # def op(self,a,b):
    #     ta = self.eindex(a)
    #     tb = self.eindex(b)

    #     return self.indexe((self.A.op(ta[0], sum(divmod(tb[0]*self.__m**ta[1],self.A.card))), self.B.op(ta[1], tb[1])))

    # def index(self,e):  # Recursive
    #     return self.A.index(e[0])+self.B.index(e[1])*self.A.card

    # def element(self,k):    # Recursive
    #     return (self.A.element(k % self.A.card), self.A.element(k//self.A.card))

    # def indexe(self, e):  # Non recursive
    #     return e[0] + e[1]*self.A.card

    # def eindex(self, k):  # Non recursive
    #     return (k % self.A.card, k//self.A.card)

    def __repr__(self):
        return "WreathCyclic("+str(self.__m)+","+str(self.__n)+")"

class WreathSymmetric(Group):
    """
    Sm≀Sn
    """
    def __init__(self,m,n):
        self.__m = m
        self.__n = n
        self.A = Direct([Symmetric(m)]*n)
        self.B = Symmetric(n)
        self.card = self.A.card*self.B.card
        self.index = lambda e: self.A.index(e[0])+self.B.index(e[1])*self.A.card
        self.element = lambda k: (self.A.element(k % self.A.card), self.A.element(k//self.A.card))
        self.op = lambda a,b: self.A.op(a%self.A.card, self.A.indexe(composition(self.B[a//self.A.card],self.A.eindex(b%self.A.card)))) + self.B.op(a//self.A.card, b//self.A.card)*self.A.card

    def __repr__(self):
        return "WreathSymmetric("+str(self.__m)+","+str(self.__n)+")"
