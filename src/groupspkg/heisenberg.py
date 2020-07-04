from groups import Group, Cyclic, Direct, Semidirect, ElementaryAbelianGroup
from sympy import isprime

def Heisenberg(p):
    return Semidirect(ElementaryAbelianGroup(p,2),Cyclic(p),lambda i: lambda k: k//p*p + (k//p*i+k)%p)

def Extraspecial(p,n,s):
    """
        p^(1+2n) extraspecial group
        s: 0 = +, 1 = -
    """
    D = ElementaryAbelianGroup(p,2*n)
    # f = [D.automorphism({})]
    pass
