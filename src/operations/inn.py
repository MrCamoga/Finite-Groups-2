from groups import Group
from group import composition

# TODO
def Inn(G, iso=0):
    """
        iso=0 subgroup of Aut(G)
        iso=1 G/Z(G)
        iso=2 subgroup of Symmetric group (the same as 0 but uses less memory)
    """
    Q = G/G.center()
    if iso & 1 == 0:
        elems = [[G.leftconjugate(g, x) for x in range(G.card)] for g in Q.reprs]

        def e(k): return elems[k]
        def op(g, h): return index(composition(e(h), e(g)))
        def index(e): return elems.index(e)

        Inn = Group(len(elems), e, op)
        Inn.index = index
        return Inn
    if iso == 1:
        return Q