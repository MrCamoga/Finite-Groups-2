from groups import Group, Direct, Semidirect
from group import composition
from operator import itemgetter


def CompleteWreath(G,H):
    """
        Let G and H be groups, G^H the set of functions from H to G.
        The complete wreath product is the semidirect product of |H| copies of G and H,
        where H acts on G^H in the following way: f∈G^H, h∈H, then f_h(x) = f(xh^-1) for all x∈H,
        (f,a)*(g,b) = (f_b*g,ab)

        This group has order |G|^|H|*|H|
    """
    D = Direct([G]*H.card)

    def act(i,k):
        inv = H.inverse(i)
        return D.indexe(tuple(itemgetter(*(H.op(j,inv) for j in H))(D[k])))
        
    return Semidirect(D,H, act)
        
class Wreath(Group):
    """
    Example:
    G = Cyclic(3)
    H = Cyclic(4)
    X = [0,1,2,3]

    A = GroupAction(H,X,{1:[1,2,3,0]})    Action of H on X

    W = Wreath(G,A)

    Let G be a group and H a group acting on a set X. The wreath product of G and H
    is {(f,h) : f:X -> G, h∈H}

    This group has order |G|^|X|*|H|

    """
    def __init__(self,G,Act):
        self._G = G
        self.D = Direct([G]*len(Act.X))
        self.H = Act.G
        self.A = Act
        self.card = self.D.card*self.H.card
        
        self.abelian = None
        self.cyclic = None
        self.simple = None
        self.id = self.indexe((self.D.identity(),self.H.identity()))
    
    def op(self,a,b):
        ta = self.eindex(a)
        tb = self.eindex(b)
        
        return self.indexe((self.D.op(ta[0], self.D.indexe(composition(self.A[ta[1]],self.D.eindex(tb[0])))), self.H.op(ta[1], tb[1])))

    def index(self,e):  # Recursive
        return self.D.index(e[0])+self.H.index(e[1])*self.D.card

    def element(self,k):    # Recursive
        return (self.D.element(k % self.D.card), self.H.element(k//self.D.card))

    def indexe(self, e):  # Non recursive
        return e[0] + e[1]*self.D.card

    def eindex(self, k):  # Non recursive
        return (k % self.D.card, k//self.D.card)

    def isSolvable(self):
        return self.D.isSolvable() and self.H.isSolvable()

    def __repr__(self):
        return "Wreath" + repr(self._G) + ","+repr(self.A)+")"
