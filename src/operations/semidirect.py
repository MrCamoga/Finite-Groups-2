from functools import reduce
from group import Group, functioninverse

class Semidirect(Group):
    """
        G⋊H
        G,H groups
        f: H -> Aut(G) hom.

        Example:
        G = Cyclic(3)
        H = Cyclic(4)

        Different ways to define the function:

        f = [[0,1,2], [0,2,1], [0,1,2], [0,2,1]]    List[List]
        f = [lambda k: k, lambda k: -k%3]*2         List[Callable]
        f = lambda i: lambda k: (-1)**i*k%3         Callable[Callable]      This is preferred since it uses less memory

        S = Semidirect(G,H,f)
    """

    def __init__(self, G, H, f):
        self.card = G.card*H.card
        self.G = G
        self.H = H

        if type(f) == list:
            if type(f[0]) == list:
                self.f = lambda k: lambda g: f[k][g]
            elif callable(f[0]):
                self.f = lambda k: f[k]
        elif callable(f):
            self.f = f

        if not (G.abelian and H.abelian):
            self.abelian = False
        else:
            self.abelian = None

        self.cyclic = None
        self.simple = False if H.card > 1 else G.simple
        self.id = self.indexe((G.identity(),H.identity()))

    def index(self, e):  # Recursive
        return self.G.index(e[0])+self.H.index(e[1])*self.G.card

    def element(self, k):  # Recursive
        return (self.G.element(k % self.G.card), self.H.element(k//self.G.card))

    def indexe(self, e):  # Non recursive
        return e[0] + e[1]*self.G.card

    def eindex(self, k):  # Non recursive
        return (k % self.G.card, k//self.G.card)

    def op(self, g1, g2):
        t1 = self.eindex(g1)
        t2 = self.eindex(g2)
        return self.indexe((self.G.op(t1[0], self.f(t1[1])(t2[0])), self.H.op(t1[1], t2[1])))

    def inverse(self, g):
        t = self.eindex(g)
        hinv = self.H.inverse(t[1])
        ginv = self.G.inverse(self.f(hinv)(t[0]))
        return self.indexe((ginv, hinv))

    """
        (g,h)^n = (g*f[h^1][g]*...*f[h^n][g],h^n) = (g', e) <=>  o(h) | n
        (g',e)^m = (g'*f[e^1][g']*...*f[e^m][g'],e) = (g'^m,e) = (e,e) <=> o(g') | m

        o((g,h)) | m*n

        o(h) = len(powersh)
        g' = reduce(...)
        o(g') = G.order(g)

        order = len(powersh)*G.order(g)
    """
    def order(self, g):
        t = self.eindex(g)
        powersh = self.H.powers(t[1])
        g = reduce(lambda a, b: self.G.op(a, b), [self.f(h)(t[0]) for h in powersh])
        return len(powersh)*self.G.order(g)

    def __repr__(self):
        return "Semidirect("+repr(self.G)+","+repr(self.H)+","+repr(self.f)+")"
