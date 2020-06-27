from groups import Group

class Dicyclic(Group):
    def __init__(self, n):
        self.card = 4*n
        self.__n = n
        twon = 2*n
        self.element = lambda k: k % self.card
        self.index = self.element
        self.op = lambda g, h: (g+h) % twon + h//twon*twon if g < twon else ((g-h+n) % twon if h >= twon else (g-h) % twon + twon)
        self.abelian = None
        self.cyclic = None

    def __repr__(self):
        return "Dicyclic("+self.__n+")"