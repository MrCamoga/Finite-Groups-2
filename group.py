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

metacyclic group
symmetric group
false witnesses group
compute orders (maybe store them) in O(n)
isIsomorphic (check cardinals, cyclic, abelian, element orders,
    conjugacy classes,... first if already computed)
isCyclic (compute orders first?) O(n)
Sylow subgroups, normal subgroups, subgroups
Aut(G), Out(G)
conjugacy classes
stabilizer
normalizer
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
        n = len(G)*len(H)
        index = lambda e: G.index(e[0])+H.index(e[1])*len(G)
        e = lambda k: (G.element(k%len(G)),H.element(k//len(G)))
        op = lambda k1,k2: G.op(k1%len(G),k2%len(G))+H.op(k1//len(G),k2//len(G))*len(G)
        GH = Group(n,e,op)
        GH.index = index
        GH.abelian = G.abelian and H.abelian
        GH.cyclic = G.cyclic and H.cyclic and gcd(len(G),len(H))==1
        return GH

    """
        G,H groups
        f: H -> Aut(G) hom.
    """
    def semidirect(G,H,f):
        n = len(G)*len(H)
        index = lambda e: G.index(e[0])+H.index(e[1])*len(G)
        e = lambda k: (G.element(k%len(G)),H.element(k//len(G)))
        op = lambda k1,k2: index((G.op(k1%len(G),f[k1//len(G)][k2%len(G)]),H.op(k1//len(G),k2//len(G))))
        GH = Group(n,e,op)
        GH.index = index
        if not (G.abelian and H.abelian):
            GH.abelian = False
        return GH

    def quotient(G,N):
        assert(G.isNormal(N))
        card = len(G)//len(N)
        cosets = [N]
        reprs = [0]
        
        for i in range(len(G)):
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
        bijection = [0]*len(G)

    """
        iso=0 subgroup of Aut(G)
        iso=1 G/Z(G)
    """
    def Inn(G, iso=0):
        Q = G.quotient(G.center())
        if iso==0:
            elems = [[G.leftconjugate(g,x) for x in range(len(G))] for g in Q.reprs]
            e = lambda k: elems[k]
            op = lambda g,h: elems.index(composition(e(h),e(g)))
            Inn = Group(len(elems),e,op)
            return Inn
        if iso==1:
            return Q
            

    def centralizer(G,s):
        return {g for g in range(len(G)) if G.op(g,s)==G.op(s,g)}

    def center(G):
        return {g for g in range(len(G)) if all({G.op(g,s)==G.op(s,g) for s in range(len(G))})}
    
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
        return {leftconjugate(g,x) for g in range(len(G))}
        
    def isSubgroup(G,H):
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
        for i in range(len(G)):
            left = set()
            right = set()
            for h in H: #optimize
                left.add(G.op(h,i))
                right.add(G.op(i,h))
            if left != right:
                return False
        return True
    
    def isAbelian(G):
        if G.abelian == None:
            S = {0}
            for g in range(len(G)):
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
        if self.index < len(self.G):
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
        T = [[G.element(G.op(j,i)) for i in range(len(G))]for j in range(len(G))]
    else:
        T = [[G.op(j,i) for i in range(len(G))]for j in range(len(G))]
    
    for i in T:
        s = ""
        for j in i:
            s += str(j)+", "
        print(s[0:-2])


def composition(f,g):
    return [g[f[x]] for x in range(len(f))]
    

def toString(T):
    print(str(T).replace("], ", "]\n").replace("[[","[").replace("]]","]"))

def gcd(a,b):
    if b==0:
        return a
    return gcd(b,a%b)
    
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
        
class Units(Group):
    def __init__(self,n):
        e = [k for k in range(1,n) if gcd(k,n)==1]
        d = {e[i]:i for i in range(len(e))}
        self.element = lambda k: e[k]
        self.index = lambda k: d[k]
        self.card = len(e)
        self.op = lambda g,h: self.index((e[g]*e[h])%n)
        self.abelian = True

if __name__ == "__main__":
    A = Cyclic(3)
    B = Dihedral(4)
    C = A*B
    cayleyTable(B)
