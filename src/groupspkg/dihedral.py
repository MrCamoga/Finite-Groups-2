from groups import Group

class Dihedral(Group):
    """
    Dihedral group: group of symmetries of an n-gon
    """
    def __init__(self, n):
        self.card = 2*n
        self.__n = n
        self.element = lambda k: k % self.card
        self.index = self.element
        self.op = lambda g, h: (g+h) % n + h//n * n if g < n else (g-h) % n + (1-h//n)*n
        self.generators = {1, n}
        self.abelian = n == 1
        self.cyclic = n == 1
        self.simple = n == 1
        self.id = 0
        self.inverse = lambda g: -g % n if g < n else g
        self.exponent = lambda: 2*n if n&1 else n

    def __repr__(self):
        return "Dihedral("+str(self.__n)+")"
