from math import gcd
from math import factorial as fact

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
normalizer                                                                      ✓

metacyclic group
alternating group
false witnesses group
compute orders (maybe store them) in O(n)
isIsomorphic (check cardinals, cyclic, abelian, element orders,
    conjugacy classes,... first if already computed)
isCyclic (compute orders first?) O(n)
Sylow subgroups, normal subgroups, subgroups
Aut(G), Out(G)
conjugacy classes
stabilizer
optimize Units()
compute automorphism given the images of generators
subset/subgroup class


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

    def direct(G,H):
        n = G.card*H.card
        index = lambda e: G.index(e[0])+H.index(e[1])*G.card
        e = lambda k: (G.element(k%G.card),H.element(k//G.card))
        op = lambda k1,k2: index(G.op(k1%G.card,k2%G.card),H.op(k1//G.card,k2//G.card))
        GH = Group(n,e,op)
        GH.index = index
        GH.abelian = G.abelian and H.abelian
        GH.cyclic = G.cyclic and H.cyclic and gcd(G.card,H.card)==1
        return GH

    def direct2(*groups):
        if len(groups)==1:
            return groups[0]
        n = reduce(lambda a,b: a*b,[G.card for G in groups])
        def e(k):
            l = []
            for G in groups:
                l.append(k%G.card)
                k //= G.card
            return tuple(l)

        def index(e):
            k = 0
            f = 1
            for i in range(len(groups)):
                k += e[i]*f
                f *= groups[i].card
            return k

        def op(g1,g2):
            t1 = e(g1)
            t2 = e(g2)
            
            return index([groups[i].op(t1[i],t2[i]) for i in range(len(groups))])

        def __coprimes():
            for i in range(len(groups)):
                for j in range(i+1,len(groups)):
                    if gcd(i,j) != 1:
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

        Q = Group(card, lambda k: cosets[k], lambda g,h: index(G.leftcoset(N,G.op(reprs[g],reprs[h]))))
        Q.reprs = reprs
        ##TODO isabelian, iscyclic
        return Q

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
        return {g for g in range(G.card) if G.leftcoset(H,g) == G.rightcoset(H,g)}

    def center(G):
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
        return G.op(G.op(g,x),G.inverse(g))
    """
        g-1xg
    """
    def rightconjugate(G,g,x):
        return G.op(G.op(G.inverse(g),x),g)

    def leftcoset(G,H,g):
        return {G.op(g,h) for h in H}

    def rightcoset(G,H,g):
        return {G.op(h,g) for h in H}

##    def conjugacyClasses(G):
        

    def conjugacyClass(G,x):
        return {leftconjugate(g,x) for g in range(G.card)}
        
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
        # if G.isSubgroup(H) and index==2: return True
        for i in range(G.card):
            left = set()
            right = set()
            for h in H: #optimize
                left.add(G.op(h,i))
                right.add(G.op(i,h))
            if left != right:
                return False
        return True

    def isNormal2(G,H): ## Faster?
        S = {}

        for h in H:
            if h in S:
               continue
            for g in range(G.card):
                if not leftconjugate(g,h) in H:
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
            if not G.abelian:
                G.cyclic = False
                return False
                #TODO
            return False

        return G.cyclic
            
    def __iter__(G):
        return GroupIter(G)

    def __truediv__(G,N):
        return G.quotient(N)
    
    def __mul__(G,H):
        return G.direct(H)

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
    return [g[f[x]] for x in range(len(f))]
    

def toString(T):
    print(str(T).replace("], ", "]\n").replace("[[","[").replace("]]","]"))
    
class Cyclic(Group):
    def __init__(self,n):
        self.element = lambda k: k%n
        self.index = self.element
        self.op = lambda g,h: (g+h)%n
        self.card = n
        self.abelian = True
        self.cyclic = True

class Dihedral(Group):
    def __init__(self,n):
        self.card = 2*n
        self.element = lambda k: k%self.card
        self.index = self.element
        self.op = lambda g,h: (g+h)%n + h//n*n if g < n else (g-h)%n + (1-h//n)*n
        self.abelian = n==1
        self.cyclic = n==1

class Dihedral2(Group): # Dihedral group as Cn⋊C2, C2 = <b> acting on Cn by bab^-1 = a^-1
    def __init__(self,n):
        D = Cyclic(n).semidirect(Cyclic(2),[[k for k in range(n)],[(n-k)%n for k in range(n)]])
        self.card = 2*n
        self.element = D.element
        self.index = D.index
        self.op = D.op
        self.abelian = n==1
        self.cyclic = n==1

class Symmetric(Group):
    def __init__(self,n):
        self.card = fact(n)
        print(self.card)
        self.__n = n
        self.element = lambda k: self.__lehmer(k)
        self.index = lambda e: self.__lehmerinv(e)
        self.op = lambda g,h: self.index(self.__permcomp(self.__lehmer(g),self.__lehmer(h)))
        self.abelian = n <= 2
        self.cyclic = n <= 2

    def center(G):
        return {0}

    def Inn(G):
        return G
    
    def __permcomp(G,g,h):
        return [g[k] for k in h]

    def __lehmerinv(G,p):
        for i in range(0,G.__n):
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
            r = k//p
            k = k%p
            code.append(r)
            p //= i

        arr = [k for k in range(0,G.__n)]
        return [arr.pop(i) for i in code]+[arr[0]]

    
class Units(Group):
    def __init__(self,n):
        e = [k for k in range(1,n) if gcd(k,n)==1]
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
    B = Dihedral(4)
    C = A*B
    cayleyTable(B)
