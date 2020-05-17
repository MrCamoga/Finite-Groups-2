from math import gcd
from math import factorial as fact
from functools import reduce
from sympy import isprime, ntheory, lcm, mod_inverse
from random import randrange
from testraster import saveImage

"""
TODO:


isNormal                                                                        ✓
Inn(G)                                                                          ✓
conjugacy class                                                                 ✓
Z(G)                                                                            ✓
centralizer                                                                     ✓
left/right cosets                                                               ✓
quotient group                                                                  ✓
powers of an element                                                            ✓
symmetric group                                                                 ✓
alternating group                                                               ✓
normalizer                                                                      ✓
commutator [g,h] = g-1h-1gh                                                     ✓
false witnesses group                                                           ✓
conjugacy classes                                                               ✓
Out(G) = Aut(G)/Inn(G)                                                          ✓
fast inverse                                                                    ✓
GL, PGL, PSL                                                                    ✓
automorphism from generators                                                    ✓
generalized symmetric group                                                     ✓
generalized quaternion group                                                    ✓
dicyclic group                                                                  ✓
central product                                                                 ✓

define group from generators and relations, for example G = < a,b,c,d | a3=b3=c3=d3=1, ab=ba, cac-1=ab-1, ad=da, bc=cb, bd=db, dcd-1=ab-1c > 
wreath produc
change the semidirect product f from array of automorphisms to an actual function
fast order for predefined groups
Write permutations as disjoint cycles (enumerate partitions of n etc), this could be useful for conjugacy classes
Change Symmetric.__lehmerinv and Alternating.__index from O(n^2) to O(n)
Change methods that treat the 0 element as the identity
metacyclic group
compute orders in O(n)
isIsomorphic (check cardinals, cyclic, abelian, element orders,
    conjugacy classes,... first if already computed)
isCyclic (compute orders first?) O(n)
Sylow subgroups, normal subgroups, subgroups
lattice of subgroups
Aut(G) (as subgroup of Sn)
get set of generators
composition series
homomorphisms class
quotient group: is abelian / is cyclic

character table
stabilizer, orbits, group action

optimize Units()
compute automorphism given the images of generators
subset/subgroup class

SL
simple groups
sporadic groups

Methods that don't work yet:
    Out(G), GL, PSL, PGL: they depend on Aut(G)


Duplicated methods/classes:

orders > orders2
centralizer2 >?? centralizer
Units2 > Units



"""

class Group:
    def __init__(self,n,e,op):
        self.element = e
        self.op = op
        self.card = n
        self.abelian = None
        self.cyclic = None

    def __len__(self):
        return self.card

    """
        two ways to call this method:
            1st: Group.direct(G1,G2,...,Gn)
            2nd: Group.direct([G1,G2,...,Gn])    i.e.   Group.direct([Cyclic(3)]*4)
    """
    def direct(*groups):
        if len(groups)==1:
            if isinstance(groups[0],Group):
                return groups[0]
            elif isinstance(groups[0],list):
                if len(groups[0]) == 1:
                    return groups[0][0]
                groups = groups[0]
        n = reduce(lambda a,b: a*b,[G.card for G in groups])
        def e(k): #Recursive, returns tuple with elements in G[i]
            l = []
            for G in groups:
                l.append(G.element(k%G.card))
                k //= G.card
            return tuple(l)

        def eindex(k): # Non recursive, returns tuple with indices in G[i]
            l = []
            for G in groups:
                l.append(k%G.card)
                k //= G.card
            return tuple(l)
        
        def index(e): # Recursive, e = tuple with elements in G[i]
            k = 0
            f = 1
            for i in range(len(groups)):
                k += groups[i].index(e[i])*f
                f *= groups[i].card
            return k

        def indexe(e): # Non recursive, e = tuple with indices in G[i]
            k = 0
            f = 1
            for i in range(len(groups)):
                k += e[i]*f
                f *= groups[i].card
            return k

        def op(g1,g2):
            t1 = eindex(g1)
            t2 = eindex(g2)
            
            return indexe([groups[i].op(t1[i],t2[i]) for i in range(len(groups))])

        def inverse(g):
            t = eindex(g)
            tinv = [groups[i].inverse(t[i]) for i in range(len(groups))]
            return indexe(tinv)

        def order(g):
            t = eindex(g)
            return lcm([groups[i].order(t[i]) for i in range(len(groups))])

        K = Group(n,e,op)
        K.index = index
        K.indexe = indexe
        K.order = order
        K.abelian = all(G.abelian for G in groups)
        K.cyclic = all(G.cyclic for G in groups) and lcm([G.card for G in groups]) == n
        K.inverse = inverse

        return K
    
    """
        G⋊H
        G,H groups
        f: H -> Aut(G) hom.
    """
    def semidirect(G,H,f):
        n = G.card*H.card
        finv = [functioninverse(aut) for aut in f]
        def index(e): # Recursive
            return G.index(e[0])+H.index(e[1])*G.card
        
        def e(k): # Recursive
            return (G.element(k%G.card),H.element(k//G.card))

        def indexe(e): # Non recursive
            return e[0] + e[1]*G.card

        def eindex(k): #Non recursive
            return (k%G.card,k//G.card)

        def op(g1,g2):
            t1 = eindex(g1)
            t2 = eindex(g2)
            return indexe((G.op(t1[0],f[t1[1]][t2[0]]), H.op(t1[1],t2[1])))
        
        GH = Group(n,e,op)
        GH.index = index

        """
            (a,b)*(c,d) = (a*f[b][c], b*d) = (e,e) <=> d = b^-1  &&  f[b][c] = a^-1
            f[b][c] = a^-1   <=>   c = f^-1[b][a^-1]
        """
        def inverse(g):
            t = eindex(g)
            hinv = H.inverse(t[1])
            ginv = finv[t[1]][G.inverse(t[0])]
            return indexe((ginv,hinv))

        """
            (g,h)^n = (g*f[h^1][g]*...*f[h^n][g],h^n) = (g', e) <=>  o(h) | n
            (g',e)^m = (g'*f[e^1][g']*...*f[e^m][g'],e) = (g'^m,e) = (e,e) <=> o(g') | m

            o((g,h)) | m*n

            o(h) = len(powersh)
            g' = reduce(...)
            o(g') = G.order(g)

            order = len(powersh)*G.order(g)
        """
        def order(g):
            t = eindex(g)
            powersh = H.powers(t[1])
            g = reduce(lambda a,b: G.op(a,b),[f[h][t[0]] for h in powersh])
            return len(powersh)*G.order(g)
            

        GH.inverse = inverse
        GH.order = order
        
        if not (G.abelian and H.abelian):
            GH.abelian = False
        return GH

    def quotient(G,N):
        assert(G.isNormal(N))
        card = G.card//len(N)
        cosets = [N]
        reprs = [0]
        
        for i in range(G.card):
            b = True
            for s in cosets:
                if i in s:
                    b = False
                    break
            if b:
                reprs.append(i)
                cosets.append(G.leftcoset(N,i))

        index = lambda e: cosets.index(e)

        Q = Group(card, lambda k: {G.element(i) for i in cosets[k]}, lambda g,h: index(G.leftcoset(N,G.op(reprs[g],reprs[h]))))
        Q.index = index
        Q.reprs = reprs
        return Q

    """
        Central product of two groups A and B with C and D central subgroups of A and B respectively
        is the quotient of AxB by the subgroup {(g,f-1(g)) : g∈A } and f : C -> D is an isomorphism
        A and B are Groups
        C and D are lists of subgroups
        f is the isomorphism viewed as a permutation. Example: f = [0,3,2,1]
    """
    def centralproduct(A,B,C,D,f):
        assert(set(C).issubset(A.center()))
        assert(set(D).issubset(B.center()))
        assert(len(C) == len(D) and len(C) == len(f))
        #todo verify f is an isomorphism
        
        AB = A*B
        Z = {AB.indexe((C[g],B.inverse(D[f[g]]))) for g in range(len(C))}

        return AB/Z

    """
        HK
    """
    def multiply(G,H,K):
        HK = set()
        for h in H:
            for k in K:
                HK.add(G.op(h,k))
        return HK

    def order(G,g):
        if g == 0:
            return 1
        order = 1
        p = g

        while True:
            p = G.op(p,g)
            order+=1
            if p==0:
                return order

    def powers(G,g):
        if g==0:
            return [0]
        p = [0,g]
        while True:
            t = G.op(p[-1],g)
            if t == 0:
                return p
            p.append(t)

    """
        Returns identity element (this method has complexity O(1) for implemeted groups since they all have the identity as the 0th element)
    """
    def identity(G):
        powers = set(G.powers(0))

        while len(powers) != 1:
            print(len(powers))
            p = set(G.powers(randrange(G.card)))
            powers = powers.intersection(p)

        return powers.pop()

    """
        get automorphism defined by the images of the generators
        genimg = {g:f(g) for g in gens}
    """
    def automorphism(G, genimg):
        bijection = [0]*G.card

        H = {0}

        for g, f in genimg.items():
            bijection[g] = f

        while len(H) != G.card:
            for g in genimg.keys():
                for h in list(H):
                    p = G.op(h,g)
                    bijection[p] = G.op(bijection[h],bijection[g])
                    H.add(p)
                
        return bijection

    #TODO
    """
        iso=0 subgroup of Aut(G)
        iso=1 G/Z(G)
        iso=2 subgroup of Symmetric group (the same as 0 but uses less memory)
    """
    def Inn(G, iso=0):
        Q = G.quotient(G.center())
        if iso&2==0:
            elems = [[G.leftconjugate(g,x) for x in range(G.card)] for g in Q.reprs]
            e = lambda k: elems[k]
            op = lambda g,h: elems.index(composition(e(h),e(g)))
            Inn = Group(len(elems),e,op)
            return Inn
        if iso==1:
            return Q
            

##    def Aut(G):
##        Aut.inverse = lambda f: Aut.index(functioninverse(f))

    def Out(G):
        return G.Aut().quotient(G.Inn())

    
    def Syl(G,p):
        if not isprime(p):
            return None
        m = G.card
        k = 0

        while m%p==0:
            m //= p
            k += 1

        order = {o for o in range(1,m+1,p) if m%o==0}
        print(order)

##        if k == 0:
##            return None
##        
            
    def centralizer(G,s):
        if G.isAbelian():
            return {g for g in range(G.card)}
        
        C = {0,s}

        H = {g for g in range(G.card)}

        while len(H) > 0:
            g = H.pop()
            if G.op(g,s) == G.op(s,g):
                powers = G.powers(g)
                C.add(g)
                for p in powers:
                    if p not in H:
                        continue
                    H.remove(p)
                    C.add(p)
        
        return C

    def centralizer2(G,s):
        return {g for g in range(G.card) if G.op(g,s)==G.op(s,g)}

    def normalizer(G,H):
        if G.isAbelian():
            return {g for g in range(G.card)}
        return {g for g in range(G.card) if G.leftcoset(H,g) == G.rightcoset(H,g)}

    def normalizer2(G,H):
        if G.isAbelian():
            return {g for g in range(G.card)}

        N = set(H)

        for g in range(len(G)):
            if g in N:
                continue
            if G.leftcoset(H,g) == G.rightcoset(H,g):
                powers = [g]
                p = G.op(g,g)
                while p not in N:
                    powers.append(p)
                    p = G.op(p,g)

                for n in list(N):
                    for m in powers:
                        N.add(G.op(n,m))
        return N
            

    def orders(G, Dict = False):
        o = {0:1}
        elements = {g for g in range(G.card)}

        while len(elements) > 0:
            g = elements.pop()
            powers = G.powers(g)
            orderg = len(powers)
            o[g] = orderg
            
            for i in range(len(powers)):
                if powers[i] in o:
                    continue
                o[powers[i]] = orderg//gcd(i,orderg)
                elements.remove(powers[i])

        if Dict:
            h = dict()
            for k,v in o.items():
                h.setdefault(v,[]).append(k)
            return h
        return [o[i] for i in range(len(G))]

    def orders2(G):
        o = {0:1}
        elements = {g for g in range(1,G.card)}

        while len(elements) > 0:
            g = elements.pop()
            p = g
            powers = [g]
            k = -1
            while True:
                t = G.op(p,g)
                if t == 0:
                    orderg = len(powers)+1
                    o[g] = orderg
                    for i in range(1,k):
                        o[powers[i]] = orderg//gcd(i+1,orderg)
                        elements.discard(powers[i])
                    break
                if t in o:
                    if len(powers) == k+1:
                        orderg = lcm(o[powers[-1]],o[t])
                        o[g] = orderg
                        for i in range(1,k):
                            o[powers[i]] = orderg//gcd(i+1,orderg)
                            elements.discard(powers[i])
                        break
                    else:
                        k = len(powers)
                p=t
                powers.append(t)
        return [o[i] for i in range(len(G))]

    def center(G):
        if G.abelian:
            return {k for k in range(G.card)}
        Z = {0}
        for g in range(G.card):
            if g in Z:
                continue
            b = False
            for s in range(G.card):
                if s in Z:
                    continue
                if G.op(s,g) != G.op(g,s):
                    b = True
                    break
            if b:
                continue
            powers = [g]
            while True:
                t = G.op(g,powers[-1])
                if t == 0 or t in S:
                    break
                powers.append(t)
            for s in list(Z):
                for x in powers:
                    Z.add(G.op(x,s))
                    
        return Z

    def pow(G,g,i): #Optimize
##        factors = ntheory.factorint(n)
        p = g;
        for i in range(i-1):
            p = G.op(p,g)
        return p;

    def inverse(G,g):
        p = g
        while True:
            tmp = G.op(p,g)
            if tmp == 0:
                return p
            p = tmp

    """
        gxg-1
    """
    def leftconjugate(G,g,x):
        return reduce(G.op, [g,x,G.inverse(g)])
    """
        g-1xg
    """
    def rightconjugate(G,g,x):
        return reduce(G.op, [G.inverse(g),x,g])

    def commutator(G,g,h):
        return reduce(G.op,[G.inverse(G.op(h,g)),g,h])

    def leftcoset(G,H,g):
        return {G.op(g,h) for h in H}

    def rightcoset(G,H,g):
        return {G.op(h,g) for h in H}
    
    def conjugacyClass(G,x):
        return {G.leftconjugate(g,x) for g in range(G.card)}

    def conjugacyClasses(G):
        Cl = []

        for i in range(G.card):
            b = False
            for C in Cl:
                if i in C:
                    b = True
                    continue
            if not b:
                Cl.append(G.conjugacyClass(i))
        return Cl
        
    def isSubgroup(G,H):
        if G.card%len(H) != 0:
            return False
        for h in H:
            for k in H:
                if G.op(h,k) not in H:
                    return False
        return True
    
    """
        Test if H is normal in G
        H = list/set with indices of elements of G
    """
    def isNormal(G,H):
        if not G.isSubgroup(H):
            return False
        if G.card == 2*len(H) or G.isAbelian():
            return True
        
        S = {}

        for h in H:
            if h in S:
               continue
            for g in range(G.card):
                if not G.leftconjugate(g,h) in H:
                    return False
            powers = [h]
            while True:
                t = G.op(h,powers[-1])
                if t == 0 or t in S:
                    break
                powers.append(t)
            for s in list(S):
                for x in powers:
                    S.add(G.op(x,s))
        return True
    
    def isAbelian(G):
        if G.abelian == None:
            S = {0}
            for g in range(G.card):
                if g in S:
                    continue
                for s in S:
                    if G.op(s,g) != G.op(g,s):
                        G.abelian = False
                        return False
                powers = [g]
                while True:
                    t = G.op(g,powers[-1])
                    if t == 0 or t in S:
                        break
                    powers.append(t)

                for s in list(S):
                    for x in powers:
                        S.add(G.op(x,s))
                
            G.abelian = True
        return G.abelian

    def isCyclic(G):
        if G.cyclic == None:
            if isPrime(G.card):
                G.cyclic = True
                G.abelian = True
                return True
            if G.isAbelian():
                print("todo")
                ##TODO
                
            else:
                G.cyclic = False
                return False

        return G.cyclic

    def isIsomorphic(G,H):
        if G.card != H.card or not (G.isAbelian() ^ H.isAbelian()) or not (G.isCyclic() ^ H.isCyclic()):
            return False
        ##TODO
            
    def __iter__(G):
        return GroupIter(G)

    def __truediv__(G,N):
        return G.quotient(N)
    
    def __mul__(G,H):
        return G.direct(H)

    def __getitem__(G,i):
        return G.element(i)
    
class GroupIter():
    def __init__(self,G):
        self.G = G
        self.index = 0
        
    def __next__(self):
        if self.index < self.G.card:
            g = self.G.element(self.index)
            self.index+=1
            return g
        raise StopIteration()
        
"""
truerepr        True prints element name
                False prints element index
"""
def cayleyTable(G, truerepr=False):
    if truerepr:
        T = [[G.element(G.op(j,i)) for i in range(G.card)]for j in range(G.card)]
    else:
        T = [[G.op(j,i) for i in range(G.card)]for j in range(G.card)]
    
    for i in T:
        s = ""
        for j in i:
            s += str(j)+", "
        print(s[0:-2])

def functioninverse(f):
    g = [0 for i in range(len(f))]
    for i in range(len(f)):
        g[f[i]] = i
    return g


def composition(f,g):
    return [g[x] for x in f]
    

def toString(T):
    print(str(T).replace("], ", "]\n").replace("[[","[").replace("]]","]"))
    
class Cyclic(Group):
    def __init__(self,n):
        self.element = lambda k: k%n
        self.index = self.element
        self.op = lambda g,h: (g+h)%n
        self.generators = {1}
        self.card = n
        self.abelian = True
        self.cyclic = True
        self.simple = isprime(n)
        self.inverse = lambda g: -g%n

    def __repr__(G):
        return "Cyclic("+str(G.card)+")"
"""
Dihedral group (symmetric of an n-gon)
"""
class Dihedral(Group):
    def __init__(self,n):
        self.card = 2*n
        self.__n = n
        self.element = lambda k: k%self.card
        self.index = self.element
        self.op = lambda g,h: (g+h)%n + h//n*n if g < n else (g-h)%n + (1-h//n)*n
        self.generators = {1,n}
        self.abelian = n==1
        self.cyclic = n==1
        self.simple = n==1
        self.inverse = lambda g: -g%n if g < n else g

    def __repr__(G):
        return "Dihedral("+str(G.__n)+")"

    
"""
Dihedral group as Cn⋊C2, C2 = <b> acting on Cn by bab^-1 = a^-1
"""
class Dihedral2(Group):
    def __init__(self,n):
        D = Cyclic(n).semidirect(Cyclic(2),[[k for k in range(n)],[(n-k)%n for k in range(n)]])
        self.card = D.card
        
        self.element = D.element
        self.index = D.index
        self.op = D.op
        self.abelian = n==1
        self.cyclic = n==1
        self.simple = n==1
        self.order = D.order

    def __repr__(G):
        return "Dihedral2("+str(G.card//2)+")"

"""
    GL(n,k): (Z/kZ)^n
"""
class GL(Group):
    def __init(self,n,k):
        G = Group.direct([Cyclic(k)]*n).Aut()
        assert(G.card == reduce(lambda a,b: a*b, [pow(k,n)-pow(k,i) for i in range(n)]))
        self.card = G.card
        self.__dim = (n,k)
        self.element = G.element
        self.index = G.index
        self.op = G.op
        self.abelian = n==1
        self.cyclic = None
        self.simple = None

    def __repr__(G):
        return "GL"+repr(G.__dim)

class PGL(Group):
    def __init__(self,n,k):
        GL = GL(n,k)
        G = GL.quotient(GL.center())
        self.card = G.card
        self.__dim = (n,k)
        self.element = G.element
        self.index = G.index
        self.op = G.op
##        self.abelian = G.abelian
##        self.cyclic = G.cyclic
##        self.simple = G.simple

"""
    GL(3,2) as subgroup of S9
"""
def GL32():
    H = list()
    det = list()
    C = Group.direct([Cyclic(2)]*3)
    S = Symmetric(C.card)
    for i in range(1,2**3):
        for j in range(1,2**3):
            if j==i:
                continue
            for k in range(1,2**3):
                if k==i or k==j or k==C.op(i,j):
                    continue
                H.append(S.index(C.automorphism({1:i,2:j,4:k})))
                v = [C[a] for a in [i,j,k]]
                det.append((v[0][0]*v[1][1]*v[2][2] + v[0][1]*v[1][2]*v[2][0] + v[1][0]*v[2][1]*v[0][2] - v[2][0]*v[1][1]*v[0][2] - v[1][0]*v[0][1]*v[2][2] - v[2][1]*v[1][2]*v[0][0])%2)

    d = {H[i]:i for i in range(len(H))}

    e = lambda k: S[H[k]]
    index = lambda e: d[S.index(e)]
    op = lambda g1,g2: d[S.op(H[g1],H[g2])]

    GL = Group(len(H),e,op)

    return GL
        
def GL23():
    H = list()
    det = list()
    C = Group.direct([Cyclic(3)]*2)
    S = Symmetric(C.card)
    for i in range(1,3**2):
        for j in range(1,3**2):
            if j==i or j==C.op(i,i):
                continue
            H.append(S.index(C.automorphism({1:i,3:j})))
            v = [C[a] for a in [i,j]]
            det.append((v[0][0]*v[1][1]-v[1][0]*v[0][1])%3)

    d = {H[i]:i for i in range(len(H))}

    e = lambda k: S[H[k]]
    index = lambda e: d[S.index(e)]
    op = lambda g1,g2: d[S.op(H[g1],H[g2])]
    

    GL = Group(len(H),e,op)

    return GL
        
        
class SL(Group):
    def __init__(self,n,k):
        GL = GL(n,k)
        G = GL.quotient()   #TODO

class PSL(Group):
    def __init__(self,n,k):
        SL = SL(n,k)
        G = SL.quotient(SL.center())
        self.card = G.card
        self.__dim = (n,k)
        self.element = G.element
        self.index = G.index
        self.op = G.op
        self.abelian = G.abelian
        self.cyclic = G.cyclic
        self.simple = n > 2 or (k!=2 and k!=3)
        
"""
Alternating group on n letters
"""
class Alternating(Group):
    def __init__(self,n):
        self.card = (fact(n)+1)//2
        self.__n = n
        self.element = self.__getperm
        self.index = lambda e: self.__index(e[:])
        self.op = lambda g,h: self.__index(composition(self[h],self[g]))
        self.abelian = n <= 3
        self.cyclic = n <= 3
        self.simple = n >= 5
        self.inverse = lambda k: self.__index(functioninverse(self.element(k)))

    def __repr__(G):
        return "Alternating("+str(G.__n)+")"
        
    def __getperm(G,k):
        p = []
        f = G.card//G.__n
        arr = [i for i in range(G.__n)]

        even = 0
        
        for i in range(G.__n-1,1,-1):
            r = k//f
            p.append(arr.pop(r))
            even += r
            k %= f
            f //= i
            
        if even%2==0:
            p += arr
        else:
            p += [arr[1],arr[0]]

        return p

    def __index(G,p):
        for i in range(len(p)-2):
            for j in range(i+1,len(p)-2):
                if p[j]>p[i]:
                    p[j] -= 1
        
        f = G.card//G.__n
        n = 0

        for i in range(len(p)-2):
            n += f*p[i]
            f //= G.__n-1-i
        return n
        
"""
Symmetric group on n letters
"""
class Symmetric(Group):
    def __init__(self,n):
        self.card = fact(n)
        self.__n = n
        self.element = self.__lehmer
        self.index = lambda e: self.__lehmerinv(e[:])
        self.op = lambda g,h: self.__lehmerinv(composition(self[h],self[g]))
##        self.generators = {self.__lehmerinv([k for k in range(n-2)]+[n-1,n-2]),self.__lehmerinv([k%n for k in range(1,n+1)])}
        self.abelian = n <= 2
        self.cyclic = n <= 2
        self.simple = n <= 2
        self.inverse = lambda k: self.__lehmerinv(functioninverse(self.element(k)))

    def __repr__(G):
        return "Symmetric("+str(G.__n)+")"

    def center(G):
        if G.__n == 2:
            return {0,1}
        return {0}

    def Inn(G):
        if G.__n == 2:
            return super().Inn()
        return G
    
    def __lehmerinv(G,p):
        for i in range(G.__n):
            for j in range(i+1,G.__n):
                if p[j]>p[i]:
                    p[j] -= 1

        f = G.card//G.__n
        n = 0

        for i in range(0,G.__n-1):
            n += f*p[i]
            f //= G.__n-1-i
        return n
        
    
    def __lehmer(G,k):
        p = G.card//G.__n
        arr = [k for k in range(G.__n)]
        perm = []
        for i in range(G.__n-1,0,-1):
            perm.append(arr.pop(k//p))
            k = k%p
            p //= i

        perm+=[arr[0]]

        return perm

"""
Multiplicative group of units modulo n

This group stores all elements in a list, and so Units2 class is preferred for big groups
"""
class Units(Group):
    def __init__(self,n):
        e = [k for k in range(1,n) if gcd(k,n)==1]
        d = {e[i]:i for i in range(len(e))}
        self.element = lambda k: e[k]
        self.index = lambda k: d[k]
##        self.index = lambda k: bisect(e,k)-1    slower (nlogn) but doesn't require inverse dictionary d
        self.card = len(e)
        self.__n = n
        self.op = lambda g,h: self.index((e[g]*e[h])%n)
        self.abelian = True
        self.inverse = lambda g: self.index(mod_inverse(e[g],n))

    def __repr__(G):
        return "Units("+str(G.__n)+")"

"""
Multiplicative group of integers modulo n up to isomorphism
"""
class Units2(Group):
    def __init__(self,n):
        factors = ntheory.factorint(n)
        l = list()

        for k,v in factors.items():
            if k==2:
                if v==1:
                    continue
                elif v==2:
                    l.append(2)
                else:
                    l += [2,2**(v-2)]
            elif v==1:
                l.append(k-1)
            else:
                l += [k-1,k**(v-1)]
        l.sort()
        groups = [Cyclic(i) for i in l]
        print([G.card for G in groups])
        G = Group.direct(groups)
        self.element = G.element
        self.index = G.index
        self.card = G.card
        self.__n = n
        self.op = G.op
        self.abelian = G.abelian
        self.cyclic = None
        self.simple = None

    def __repr__(G):
        return "Units2("+str(G.__n)+")"

"""
Subgroup of multiplicative group of integers mod n

We know from FLT that for p prime and x=1,...,p-1    x^(p-1) = 1 (mod p)
If n is composite and x verifies that equality, we say that x is a false witness for n.

The set of all false witnesses mod n is a subgroup.
"""
class FalseWitness(Group):
    def __init__(self,n):
        e = [k for k in range(1,n) if pow(k,n-1,n)==1]
        d = {e[i]:i for i in range(len(e))}
        self.element = lambda k: e[k]
        self.index = lambda k: d[k]
        self.card = len(e)
        self.__n = n
        self.op = lambda g,h: self.index((e[g]*e[h])%n)
        self.abelian = True
        self.inverse = lambda k: self.index(mod_inverse(e[k],n))

    def __repr__(G):
        return "FalseWitness("+str(G.__n)+")"


"""
The generalized symmetric group is the wreath product Zm≀Sn = (Zm)^n⋊φSn
with Sn acting on (Zm)^n by φ(σ)(a1,..., an) := (aσ(1),..., aσ(n))

"""
class GeneralizedSymmetric(Group):
    def __init__(self,m,n):
        S = Symmetric(n)
        C = Group.direct([Cyclic(m)]*n)
        
        self.card = S.card*C.card
        self.index = lambda e: C.index(e[0]) + S.index(e[1])*C.card
        self.element = lambda k: (C[k%C.card], S[k//C.card])
        self.op = lambda k1,k2: C.op(k1%C.card, C.index(composition(S[k1//C.card],C[k2%C.card]))) + S.op(k1//C.card, k2//C.card)*C.card
        self.abelian = None
        self.cyclic = None

class GeneralizedQuaternion(Group):
    def __init__(self,k):
        self.card = 2**(k+1)
        n = self.card//2
        self.element = lambda k: k&(self.card-1)
        self.index = self.element
        self.op = lambda g,h: (g+h)%n + h//n*n if g < n else ( (g-h+n//2)%n if h >= n else (g-h)%n + n)
        self.abelian = None

class Dicyclic(Group):
    def __init__(self,n):
        self.card = 4*n
        twon = 2*n
        self.element = lambda k: k%self.card
        self.index = self.element
        self.op = lambda g,h: (g+h)%twon + h//twon*twon if g < twon else ( (g-h+n)%twon if h >= twon else (g-h)%twon + twon)
        self.abelian = None
        
class Subset():
    def __init__(self,G,H):
        e = list(H)
        self.element = lambda k: e[k]
        self.card = len(H)
        self.op = lambda g,h: G.op(self.element(g),self.element(h)) ## This returns an element of G that cannot be converted back to an element of H since we don't know of H is closed under the operation of G
        self.subgroup = None

##if __name__ == "__main__":
    
