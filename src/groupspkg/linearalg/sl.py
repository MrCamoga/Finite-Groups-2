from groups import Group, GL, Cyclic

def SL(n, k):
    G = GL(n, k).derivedSubgroup()
    G.__dim = (n,k)
    G.abelian = None
    G.cyclic = None
    G.simple = None
    G.id = None
    G.field = Cyclic(k)**n

    return G
