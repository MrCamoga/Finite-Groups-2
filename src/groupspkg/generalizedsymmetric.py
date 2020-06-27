from group import composition
from groups import Symmetric, Cyclic, Direct, Group

class GeneralizedSymmetric(Group):
    """
    The generalized symmetric group is the wreath product Zm≀Sn = (Zm)^n⋊φSn
    with Sn acting on (Zm)^n by φ(σ)(a1,..., an) := (aσ(1),..., aσ(n))
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
