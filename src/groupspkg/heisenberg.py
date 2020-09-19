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
        p^(1+2n)_{±} extraspecial group is a p-group G with center Z of order p and G/Z elementary abelian ((Cp)^2n)
        There are two extraspecial groups up to isomorphism: '+' has exponent p and '-' has exponent p^2
        
        s: sign, 0 = +, 1 = -
    """
    assert(isprime(p))

    if n==1:
        if s==0:
            return Semidirect(Cyclic(p)**2,Cyclic(p), lambda c,e: e//p*p + (e//p*c+e)%p)
        if s==1:
            return Semidirect(Cyclic(p**2),Cyclic(p), lambda c,e: (p+1)**c*e%(p**2))
    elif n>1:
        if s==0:
            G = Extraspecial(p,1,0)
            C = G**n
            Q = C/{C.indexe([i]*n) for i in range(p)}
            return Q
        if s==1:
            G = Extraspecial(p,1,0)
            H = Extraspecial(p,1,1)
            C = Direct([G]*(n-1)+[H])
            Q = C/{C.indexe([i]*(n-1)+[p*i]) for i in range(p)}
            return Q
