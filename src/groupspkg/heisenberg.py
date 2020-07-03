from groups import Group, Cyclic, Direct, Semidirect, ElementaryAbelianGroup
from sympy import isprime

def Heisenberg(p):
    D = ElementaryAbelianGroup(p,2)
    f = lambda i: lambda k: k//p*p + (k//p*i+k)%p           # O(1) memory usage
    # f = [D.automorphism({1:1,p:(p+k)}) for k in range(0,p)]     # O(p^3) memory usage
    return Semidirect(D,Cyclic(p),f)

def Extraspecial(p,n,s):
    """
        p^(1+2n) extraspecial group
        s: 0 = +, 1 = -
    """
    D = ElementaryAbelianGroup(p,2*n)
    # f = [D.automorphism({})]
    pass
