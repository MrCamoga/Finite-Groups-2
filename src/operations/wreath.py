from groups import Group, Direct
from group import composition

class Wreath(Group):
    """
    Example:
    G = Cyclic(3)
    H = Cyclic(4)
    X = [0,1,2,3]

    A = GroupAction(H,X,{1:[1,2,3,0]})    Action of H on X

    W = Wreath(G,A)

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

    def __repr__(self):
        return "Wreath" + repr(self._G) + ","+repr(self.A)+")"