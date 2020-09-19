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
    return Extraspecial(p,1,0)

def Extraspecial(p,n,s):
    """
        p^(1+2n) extraspecial group
        s: 0 = +, 1 = -
    """
    D = ElementaryAbelianGroup(p,2*n)
    # f = [D.automorphism({})]

    if n==1:
        if s==0:
            return Semidirect(Cyclic(p)**2,Cyclic(p), lambda c,e: e//p*p + (e//p*c+e)%p)
        if s==1:
            return Semidirect(Cyclic(p**2),Cyclic(p), lambda c,e: (p+1)**c*e%(p**2))
    elif n>1:
        if s==0:
            # Central product of n p^3_+
        if s==1:
            # Central product of n-1 p^3_+ and p^3_-
