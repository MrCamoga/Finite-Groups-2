from groups import Group, Cyclic, Direct, Semidirect, ElementaryAbelianGroup
from sympy import isprime

def Heisenberg(p):
    """
    Group of 3x3 upper triangular matrices with unit determinant modulo p

    Element of the group ((a,b),c) corresponds with matrix:
        1 b a 
        0 1 c
        0 0 1

    Operation of matrices:
        AB = op(B,A)
    """
    return Semidirect(ElementaryAbelianGroup(p,2),Cyclic(p),lambda i, k: k//p*p + (k//p*i+k)%p)

def Extraspecial(p,n,s):
    """
        p^(1+2n) extraspecial group
        s: 0 = +, 1 = -
    """
    D = ElementaryAbelianGroup(p,2*n)
    # f = [D.automorphism({})]
    pass
