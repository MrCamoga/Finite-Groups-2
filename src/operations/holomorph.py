from groups import Semidirect, Aut2

"""
    The holomorph of a group G is the semmidirect product of G and Aut(G)
    This group contains G as a normal subgroup and all automorphisms of G
    are restrictions of inner automorphisms
"""
def Holomorph(G):
    A = Aut2(G)
    
    return Semidirect(G,A, lambda a,g: A[A.inverse(a)][g])
