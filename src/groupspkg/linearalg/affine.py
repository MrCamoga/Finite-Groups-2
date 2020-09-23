from groups import Semidirect, GL, SL
from sympy import isprime

def AGL(n,k):
    """
        Affine linear group: group of affine invertible transformations on Z_k^n
        AGL(n,k) = (Z_n)^k ⋊ GL(n,k)
    """
    assert(isprime(k))
    G = GL(n,k)
    return Semidirect(G.field,G, lambda g,v: G[G.inverse(g)][v])

def ASL(n,k):
    """
        Affine special linear group: group of affine transformations 
        ASL(n,k) = (Z_n)^k ⋊ SL(n,k)
    """
    assert(isprime(k))
    G = SL(n,k)
    return Semidirect(G.field,G, lambda g,v: G[G.inverse(g)][v])
