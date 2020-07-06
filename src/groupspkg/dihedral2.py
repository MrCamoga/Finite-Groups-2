from groups import Cyclic, Semidirect, Group

class Dihedral2(Group):
    """
    Dihedral group as Cn⋊C2, C2 = <b> acting on Cn by bab^-1 = a^-1
    """
    def __init__(self, n):
        # f = [[k for k in range(n)], [(n-k) % n for k in range(n)]]
        f = lambda i, k: -k%n if i == 1 else k
        D = Semidirect(Cyclic(n), Cyclic(2), f)
        self.card = D.card

        self.element = D.element
        self.index = D.index
        self.op = D.op
        self.abelian = n == 1
        self.cyclic = n == 1
        self.simple = n == 1
        self.id = 0
        self.order = D.order

    def __repr__(self):
        return "Dihedral2("+str(self.card//2)+")"

