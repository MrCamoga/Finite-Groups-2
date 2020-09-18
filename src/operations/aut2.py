from group import functioninverse, composition
from groups import Group, Homomorphism
from operator import itemgetter
from bisect import bisect_left

def Aut2(G, gens = None):
    """
        Group or automorphisms of G
        gens: set/list with generators of G
    """
    if gens is None:
        gens = G.generators
    gens = sorted(list(gens))
    aut = [(0,)*len(gens)]
    
    ordersd = G.orders(True)
    genorders = [G.order(g) for g in gens]
    
    for i in range(len(gens)):
        newaut = []
        for a in aut:
            H = G.subgroup(a)
            for fg in ordersd[genorders[i]] - H:
                automorphism = list(a)
                automorphism[i] = fg
                if set(G.powers(fg)).intersection(H) == {G.identity()}:
                    newaut.append(tuple(automorphism))
                
        del aut
        aut = newaut

    # automorphisms = []

    # for i,a in enumerate(aut):
    #     f = Homomorphism(G,G,{gens[i]:a[i] for i in range(len(gens))})
    #     if not f.isIsomorphism():
    #         aut.remove(a)
    #     else:
    #         automorphisms.append(f._f)

    aut.sort(key = itemgetter(*(k for k in range(len(gens)))))

    automorphisms = [G.automorphism({g:a[i] for i,g in enumerate(gens)}) for a in aut]

    def e(k):
        return automorphisms[k]
        # return aut[k]

    def index(e):
        return bisect_left(aut,e)

    # def op2(a,b):
    #     """
    #         a*b = b◦a
    #     """

    #     fb = automorphisms[b]
    #     c = [fb[aut[a][i]] for i in range(len(gens))]
    #     return index(c)

    def op(a,b):
        """
            a*b = b◦a
        """
        return index(itemgetter(*aut[a])(automorphisms[b]))

    # def inverse(f):


    # def op(a,b):
        
    #     fa = automorphisms[a]
    #     fb = automorphisms[b]
    #     fc = composition(fa,fb)
    #     c = [fc[i] for i in gens]
    #     return index(c)

    Aut = Group(len(aut), e, op)
    Aut.index = index
    Aut.inverse = lambda f: index(itemgetter(*gens)(functioninverse(automorphisms[f])))
    Aut.gens = gens
    Aut.group = G
    Aut.aut = aut
    Aut.generators = None
    
    return Aut
