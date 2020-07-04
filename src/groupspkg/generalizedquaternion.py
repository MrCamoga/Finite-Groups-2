from groups import Group

class GeneralizedQuaternion(Group):
    def __init__(self, k):
        self.card = 2**(k+1)
        n = self.card//2
        self.__n = k
        self.element = lambda k: k & (self.card-1)
        self.index = self.element
        self.op = lambda g, h: (g+h) % n + h//n*n if g < n else ((g-h+n//2) % n if h >= n else (g-h) % n + n)
        self.generators = {1,n}
        self.abelian = None
        self.cyclic = None
        self.simple = None
        self.id = 0

    def __repr__(self):
        return "GeneralizedQuaternion("+self.__n+")"