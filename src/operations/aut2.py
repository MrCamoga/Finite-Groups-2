from group import functioninverse, composition
from groups import Group
from operator import itemgetter
from bisect import bisect_left

def Aut2(G, gens = None):
    """
        Group or automorphisms of G
        gens: set/list with generators of G
    """
    if gens is None:
        gens = G.generators
    gens = list(gens)
    aut = [[0]*len(gens)]
    
    ordersd = G.orders(True)
    genorders = [G.order(g) for g in gens]

    for i in range(len(gens)):
        newaut = []
        for a in aut:
            for fg in ordersd[genorders[i]] - G.subgroup(a):
                automorphism = list(a)
                automorphism[i] = fg
                newaut.append(automorphism)
                
        del aut
        aut = newaut

    aut.sort(key = itemgetter(*(k for k in range(len(gens)))))

    def e(k):
        return aut[k]

    def index(e):
        return bisect_left(aut,e)

    automorphisms = [G.automorphism({g:a[i] for i,g in enumerate(gens)}) for a in aut]

    def op(a,b):
        """
            a*b = b◦a
        """
        fb = automorphisms[b]
        c = [fb[aut[a][i]] for i in range(len(gens))]
        return index(c)

    Aut = Group(len(aut), e, op)
    Aut.index = index
    Aut.inverse = lambda f: index(list(itemgetter(*gens)(functioninverse(automorphisms[f]))))
    
    return Aut