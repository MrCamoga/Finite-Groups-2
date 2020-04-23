from math import gcd
from math import factorial as fact
from functools import reduce
from sympy import isprime, ntheory, lcm

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

metacyclic group
compute orders (maybe store them) in O(n)
isIsomorphic (check cardinals, cyclic, abelian, element orders,
    conjugacy classes,... first if already computed)
isCyclic (compute orders first?) O(n)
Sylow subgroups, normal subgroups, subgroups
Aut(G) (as subgroup of Sn)
Out(G) = Aut(G)/Inn(G)
store set of generators
conjugacy classes

character table
stabilizer, orbits, group action

optimize Units()
compute automorphism given the images of generators
subset/subgroup class

SL, PSL, PGL
simple groups
sporadic groups


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

        def __coprimes():
            for i in range(len(groups)):
                for j in range(i+1,len(groups)):
                    if gcd(groups[i].card,groups[j].card) != 1:
                        return False
            return True

        K = Group(n,e,op)
        K.index = index
        K.abelian = all(G.abelian for G in groups)
        K.cyclic = all(G.cyclic for G in groups) and __coprimes()

        return K
    
    """
        G,H groups
        f: H -> Aut(G) hom.
    """
    def semidirect(G,H,f):
        n = G.card*H.card
        index = lambda e: G.index(e[0])+H.index(e[1])*G.card
        e = lambda k: (G.element(k%G.card),H.element(k//G.card))
        op = lambda k1,k2: index((G.op(k1%G.card,f[k1//G.card][k2%G.card]),H.op(k1//G.card,k2//G.card)))
        GH = Group(n,e,op)
        GH.index = index
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
            for s in cosets: # Check if i already in one coset
                if i in s:
                    b = False
                    break
            if b:
                reprs.append(i)
                cosets.append(G.leftcoset(N,i))

        index = lambda e: cosets.index(e)

        Q = Group(card, lambda k: {G.element(i) for i in cosets[k]}, lambda g,h: index(G.leftcoset(N,G.op(reprs[g],reprs[h]))))
        Q.reprs = reprs
        ##TODO isabelian, iscyclic
        return Q

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
        
    #TODO
    def automorphism(G, genimg):
        bijection = [0]*G.card

    """
        iso=0 subgroup of Aut(G)
        iso=1 G/Z(G)
    """
    def Inn(G, iso=0):
        Q = G.quotient(G.center())
        if iso==0:
            elems = [[G.leftconjugate(g,x) for x in range(G.card)] for g in Q.reprs]
            e = lambda k: elems[k]
            op = lambda g,h: elems.index(composition(e(h),e(g)))
            Inn = Group(len(elems),e,op)
            return Inn
        if iso==1:
            return Q
            
    def centralizer(G,s):
        return {g for g in range(G.card) if G.op(g,s)==G.op(s,g)}

    def normalizer(G,H):
        if G.isAbelian():
            return H
        return {g for g in range(G.card) if G.leftcoset(H,g) == G.rightcoset(H,g)}

    def orders(G):
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

##        h = dict()
##        for k,v in o.items():
##            h.setdefault(v,[]).append(k)
##        return h
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

##    def conjugacyClasses(G):
        

    def conjugacyClass(G,x):
        return {G.leftconjugate(g,x) for g in range(G.card)}
        
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
        if not G.isSubgroup(H): # Unnecessary?
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

"""
Dihedral group (symmetric of an n-gon)
"""
class Dihedral(Group):
    def __init__(self,n):
        self.card = 2*n
        self.element = lambda k: k%self.card
        self.index = self.element
        self.op = lambda g,h: (g+h)%n + h//n*n if g < n else (g-h)%n + (1-h//n)*n
        self.generators = {1,n}
        self.abelian = n==1
        self.cyclic = n==1
        self.simple = n==1

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

"""
    GL(n,k): (Z/kZ)^n
"""
class GL(Group):
    def __init(self,n,k):
        G = Group.direct([Cyclic(k)]*n).Aut()
        assert(G.card == reduce(lambda a,b: a*b, [pow(k,n)-pow(k,i) for i in range(n)]))
        self.card = G.card
        self.element = G.element
        self.index = G.index
        self.op = G.op
        self.abelian = n==1
        self.cyclic = None
        self.simple = None

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
        self.generators = {self.__lehmerinv([k for k in range(n-2)]+[n-1,n-2]),self.__lehmerinv([k%n for k in range(1,n+1)])}
        self.abelian = n <= 2
        self.cyclic = n <= 2
        self.simple = n <= 2

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
        code = []
        for i in range(G.__n-1,0,-1):
            code.append(k//p)
            k = k%p
            p //= i

        arr = [k for k in range(G.__n)]
        return [arr.pop(i) for i in code]+[arr[0]]

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
        self.card = len(e)
        self.op = lambda g,h: self.index((e[g]*e[h])%n)
        self.abelian = True

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
        self.op = G.op
        self.abelian = G.abelian
        self.cyclic = None
        self.simple = None

"""
Subgroup of multiplicative group of integers mod n

We know from FLT that for a p prime and x=1,...,p-1    x^(p-1) = 1 (mod p)
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
        self.op = lambda g,h: self.index((e[g]*e[h])%n)
        self.abelian = True

class Subset():
    def __init__(self,G,H):
        e = list(H)
        self.element = lambda k: e[k]
        self.card = len(H)
        self.op = lambda g,h: G.op(self.element(g),self.element(h)) ## This returns an element of G that cannot be converted back to an element of H since we don't know of H is closed under the operation of G
        self.subgroup = None

if __name__ == "__main__":
    A = Cyclic(3)
##    B = Dihedral(4)
##    C = A*B
##    cayleyTable(B)
    
