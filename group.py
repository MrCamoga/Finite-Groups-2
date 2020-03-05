"""
TODO:

metacyclic group
symmetric group
false witnesses group
compute orders (maybe store them) in O(n)
isNormal
isIsomorphic (check cardinals, cyclic, abelian, element orders, conjugacy classes,... first if already computed)
isCyclic (compute orders first?) O(n)
Sylow subgroups, normal subgroups, subgroups
Aut(G), Inn(G), Out(G)
conjugacy classes
Z(G)
stabilizer
centralizer
normalizer
optimize Units()
left/right cosets
compute automorphism given the images of generators

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
        e = lambda k: (G.element(k%len(G)),H.element(k//len(G)))
        op = lambda k1,k2: G.op(k1%len(G),k2%len(G))+H.op(k1//len(G),k2//len(G))*len(G)
        GH = Group(n,e,op)
        GH.abelian = G.abelian and H.abelian
        GH.cyclic = G.cyclic and H.cyclic and gcd(len(G),len(H))==1
        return GH

    """
        G,H groups
        f: H -> Aut(G) hom.
    """
    def semidirect(G,H,f):
        n = len(G)*len(H)
        e = lambda k: (G.element(k%len(G)),H.element(k//len(G)))
        op = lambda k1,k2: G.op(k1%len(G),f[k1//len(G)][k2%len(G)])+H.op(k1//len(G),k2//len(G))*len(G)

    """
        Test if H is normal in G
        H = list/set with indices of elements of G
    """
    def isNormal(G,H):
        #TODO
        return
    
    def isAbelian(G):
        if G.abelian == None:
            for i in range(len(G)):
                for j in range(i,len(G)):
                    if G.op(i,j) != G.op(j,i):
                        G.abelian = False
                        return False
            G.abelian = True
            return True
        return G.abelian

    def isCyclic(G):
        if G.cyclic == None:
            if not G.abelian:
                G.cyclic = False
                return False
                #TODO
            return False

        return G.cyclic
            

    def __mul__(G,H):
        return G.direct(H)

"""
truerepr        True prints element name
                False prints element index
"""
def cayleyTable(G, truerepr=False):
    if truerepr:
        T = [[G.element(G.op(j,i)) for i in range(len(G))]for j in range(len(G))]
    else:
        T = [[G.op(j,i) for i in range(len(G))]for j in range(len(G))]
    
    print(str(T).replace("], ", "]\n").replace("[[","[").replace("]]","]"))

def gcd(a,b):
    if b==0:
        return a
    return gcd(b,a%b)
    
class Cyclic(Group):
    def __init__(self,n):
        self.element = lambda k: k%n
        self.op = lambda g,h: (g+h)%n
        self.card = n
        self.abelian = True
        self.cyclic = True

class Dihedral(Group):
    def __init__(self,n):
        self.card = 2*n
        self.element = lambda k: k%self.card
        self.op = lambda g,h: (g+h)%n + h//n*n if g < n else (g-h)%n + (1-h//n)*n
        self.abelian = n==1
        self.cyclic = n==1
        
class Units(Group):
    def __init__(self,n):
        e = [k for k in range(1,n) if gcd(k,n)==1]
        d = {e[i]:i for i in range(len(e))}
        self.element = lambda k: e[k]
        self.card = len(e)
        self.op = lambda g,h: d[(e[g]*e[h])%n]
        self.abelian = True

if __name__ == "__main__":
    A = Cyclic(3)
    B = Cyclic(3)
    C = A*B
    cayleyTable(C)
