from group import functioninverse, composition
from groups import Group

def Aut(G, gens = None):
    """
        Group or automorphisms of G
        gens: set/list with generators of G
    """

    aut = [dict()]

    if gens is None:
        gens = G.generators
    gens = list(gens)
    
    ordersd = G.orders(True)
    genorders = [G.order(g) for g in gens]
    print(genorders)
    for g in range(len(gens)):
        newaut = []
        for a in aut:
            R = ordersd[genorders[g]] - G.subgroup(a.values())
            for fg in R:
                automorphism = dict(a)
                automorphism[gens[g]] = fg
                newaut.append(automorphism)
                
        del aut
        aut = newaut
        print(len(aut))

    def e(k):
        return aut[k]

    def index(e):
        return aut.index(e)

    automorphisms = [G.automorphism(a) for a in aut]

    def op(a,b):
        """
            a*b = b◦a
        """
        fb = automorphisms[b]
        c = {i:fb[aut[a][i]] for i in gens}
        return index(c)

    Aut = Group(len(aut), e, op)
    Aut.index = index
    Aut.inverse = lambda f: index(functioninverse(automorphisms(f)))
    
    return Aut
