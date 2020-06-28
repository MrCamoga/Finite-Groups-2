from group import functioninverse, composition
from groups import Group

def Aut(G, gens = None):
    """
        Group or automorphisms of G
        gens: set/list with generators of G
    """

    automorphisms = [dict()]

    if gens is None:
        gens = G.generators()
    gens = list(gens)
    
    ordersd = G.orders(True)
    genorders = [G.order(g) for g in gens]

    for g in range(len(gens)):
        newaut = []
        for a in automorphisms:
            R = ordersd[genorders[g]] - G.subgroup(a.values())
            for fg in R:
                automorphism = dict(a)
                automorphism[gens[g]] = fg
                newaut.append(automorphism)
                
        del automorphisms
        automorphisms = newaut

    def e(k):
        return automorphisms[k]

    def index(e):
        return automorphisms.index(e)

    def op(a,b):
        """
            a*b = b◦a
        """
        fa = G.automorphism(automorphisms[a])
        fb = G.automorphism(automorphisms[b])
        fc = composition(fa,fb)
        c = {i:fc[i] for i in gens}
        return index(c)

    Aut = Group(len(automorphisms), e, op)
    Aut.index = index
    Aut.inverse = lambda f: index(functioninverse(G.automorphism(Aut[f])))
    
    return Aut
