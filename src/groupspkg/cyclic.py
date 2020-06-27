from sympy import isprime
from groups import Group

class Cyclic(Group):
    def __init__(self, n):
        self.element = lambda k: k % n
        self.index = self.element
        self.op = lambda g, h: (g+h) % n
        self.generators = {1}
        self.card = n
        self.abelian = True
        self.cyclic = True
        self.simple = isprime(n)
        self.inverse = lambda g: -g % n

    def __repr__(self):
        return "Cyclic("+str(self.card)+")"
