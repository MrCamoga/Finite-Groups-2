from math import gcd
from math import factorial as fact
from functools import reduce
from sympy import isprime, ntheory, lcm, mod_inverse
from random import randrange


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
homomorphisms class                                                             ✓
subset/subgroup class                                                           ✓
isCyclic                                                                        ✓

define group from generators and relations, for example G = < a,b,c,d | a3=b3=c3=d3=1, ab=ba, cac-1=ab-1, ad=da, bc=cb, bd=db, dcd-1=ab-1c > 
wreath product
change Group.card into a function
change the semidirect product f from array of automorphisms to an actual function
    define GeneralizedSymmetric group with Group.semidirect
fast order for predefined groups
Write permutations as disjoint cycles (enumerate partitions of n etc), this could be useful for conjugacy classes
Change Symmetric.__lehmerinv and Alternating.__index from O(n^2) to O(n)
Change methods that treat the 0 element as the identity
metacyclic group
compute orders in O(n)
isIsomorphic (check cardinals, cyclic, abelian, element orders,
    conjugacy classes,...)
isSimple
Sylow subgroups, normal subgroups, subgroups
commutator subgroup
lattice of subgroups
Aut(G) (as subgroup of Sn)
get set of generators
composition series
lower central series
quotient group: is abelian / is cyclic / simple

character table
stabilizer, orbits, group action

optimize Units()
compute automorphism given the images of generators

SL
simple groups
sporadic groups

Methods that don't work yet:
    Out(G), GL, SL, PSL, PGL: they depend on Aut(G)


Duplicated methods/classes:

orders > orders2
centralizer2 >?? centralizer
Units2 > Units
"""

class Group:
    def __init__(self, n, e, op):
        self.element = e
        self.op = op
        self.card = n
        self.abelian = None
        self.cyclic = None
        self.simple = None

    def __len__(self):
        return self.card

    def multiply(self, H, K):
        """
            HK = {h*k : h∈H, k∈K}
        """
        HK = set()
        for h in H:
            for k in K:
                HK.add(self.op(h, k))
        return HK

    def order(self, g):
        if g == 0:
            return 1
        order = 1
        p = g

        while True:
            p = self.op(p, g)
            order += 1
            if p == 0:
                return order

    def powers(self, g):
        """
            <g> = {g^k : k∈N}
        """
        if g == 0:
            return [0]
        p = [0, g]
        while True:
            t = self.op(p[-1], g)
            if t == 0:
                return p
            p.append(t)

    """
        Returns identity element (this method has complexity O(1) for implemented groups since they all have the identity as the 0th element)
    """
    def identity(self):
        powers = set(self.powers(0))

        while len(powers) != 1:
            print(len(powers))
            p = set(self.powers(randrange(self.card)))
            powers = powers.intersection(p)

        return powers.pop()

    def automorphism(self, genimg):
        """
            Get automorphism defined by the images of the generators
            genimg = {g:f(g) for g in gens}
        """
        bijection = [0]*self.card

        H = {0}

        for g, f in genimg.items():
            bijection[g] = f

        while len(H) != self.card:
            for g in genimg.keys():
                for h in list(H):
                    p = self.op(h, g)
                    bijection[p] = self.op(bijection[h], bijection[g])
                    H.add(p)

        return bijection

    def Syl(self, p):
        if not isprime(p):
            return None
        m = self.card
        k = 0

        while m % p == 0:
            m //= p
            k += 1

        order = {o for o in range(1, m+1, p) if m % o == 0}

        # if k == 0:
        # return None
        ##

    def centralizer(self, s):
        """
            {g∈G : gs=sg ∀s∈G}
        """
        if self.isAbelian():
            return {g for g in range(self.card)}

        C = {0, s}

        H = {g for g in range(self.card)}

        while len(H) > 0:
            g = H.pop()
            if self.op(g, s) == self.op(s, g):
                powers = self.powers(g)
                C.add(g)
                for p in powers:
                    if p not in H:
                        continue
                    H.remove(p)
                    C.add(p)

        return C

    def centralizer2(self, s):
        return {g for g in range(self.card) if self.op(g, s) == self.op(s, g)}

    def normalizer(self, H):
        if self.isAbelian():
            return {g for g in range(self.card)}
        return {g for g in range(self.card) if self.leftcoset(H, g) == self.rightcoset(H, g)}

    def normalizer2(self, H):
        if self.isAbelian():
            return {g for g in range(self.card)}

        N = set(H)

        for g in range(len(self)):
            if g in N:
                continue
            if self.leftcoset(H, g) == self.rightcoset(H, g):
                powers = [g]
                p = self.op(g, g)
                while p not in N:
                    powers.append(p)
                    p = self.op(p, g)

                for n in list(N):
                    for m in powers:
                        N.add(self.op(n, m))
        return N

    def orders(self, Dict=False):
        o = {0: 1}
        elements = {g for g in range(self.card)}

        while len(elements) > 0:
            g = elements.pop()
            powers = self.powers(g)
            orderg = len(powers)
            o[g] = orderg

            for i in range(len(powers)):
                if powers[i] in o:
                    continue
                o[powers[i]] = orderg//gcd(i, orderg)
                elements.remove(powers[i])

        if Dict:
            h = dict()
            for k, v in o.items():
                h.setdefault(v, []).append(k)
            return h
        return [o[i] for i in range(len(self))]

    def orders2(self):
        o = {0: 1}
        elements = {g for g in range(1, self.card)}

        while len(elements) > 0:
            g = elements.pop()
            p = g
            powers = [g]
            k = -1
            while True:
                t = self.op(p, g)
                if t == 0:
                    orderg = len(powers)+1
                    o[g] = orderg
                    for i in range(1, k):
                        o[powers[i]] = orderg//gcd(i+1, orderg)
                        elements.discard(powers[i])
                    break
                if t in o:
                    if len(powers) == k+1:
                        orderg = lcm(o[powers[-1]], o[t])
                        o[g] = orderg
                        for i in range(1, k):
                            o[powers[i]] = orderg//gcd(i+1, orderg)
                            elements.discard(powers[i])
                        break
                    else:
                        k = len(powers)
                p = t
                powers.append(t)
        return [o[i] for i in range(len(self))]

    def center(self):
        if self.abelian:
            return {k for k in range(self.card)}
        Z = {0}
        for g in range(self.card):
            if g in Z:
                continue
            b = False
            for s in range(self.card):
                if s in Z:
                    continue
                if self.op(s, g) != self.op(g, s):
                    b = True
                    break
            if b:
                continue
            powers = [g]
            while True:
                t = self.op(g, powers[-1])
                if t == 0 or t in Z:
                    break
                powers.append(t)
            for s in list(Z):
                for x in powers:
                    Z.add(self.op(x, s))

        return Z

    def pow(self, g, i):
        """
            g^i
        """
        p = 0
        while i > 0:
            if i & 1:
                p = self.op(p, g)
            g = self.op(g, g)
            i >>= 1
        return p

    def inverse(self, g):
        p = g
        while True:
            tmp = self.op(p, g)
            if tmp == 0:
                return p
            p = tmp

    def leftconjugate(self, g, x):
        """
            gxg-1
        """
        return reduce(self.op, [g, x, self.inverse(g)])

    def rightconjugate(self, g, x):
        """
            g-1xg
        """
        return reduce(self.op, [self.inverse(g), x, g])

    def commutator(self, g, h):
        """
            g-1h-1gh
        """
        return reduce(self.op, [self.inverse(self.op(h, g)), g, h])

    def leftcoset(self, H, g):
        return {self.op(g, h) for h in H}

    def rightcoset(self, H, g):
        return {self.op(h, g) for h in H}

    def conjugacyClass(self, x):
        return {self.leftconjugate(g, x) for g in range(self.card)}

    def conjugacyClasses(self):
        Cl = []

        for i in range(self.card):
            b = False
            for C in Cl:
                if i in C:
                    b = True
                    continue
            if not b:
                Cl.append(self.conjugacyClass(i))
        return Cl

    def isSubgroup(self, H):
        if self.card % len(H) != 0:
            return False
        for h in H:
            for k in H:
                if self.op(h, k) not in H:
                    return False
        return True

    def isNormal(self, H):
        """
            Test if H is normal in G
            H = list/set with indices of elements of G
        """
        if not self.isSubgroup(H):
            return False
        if self.card == 2*len(H) or self.isAbelian():
            return True

        S = set()

        for h in H:
            if h in S:
                continue
            for g in range(self.card):
                if not self.leftconjugate(g, h) in H:
                    return False
            powers = [h]
            while True:
                t = self.op(h, powers[-1])
                if t == 0 or t in S:
                    break
                powers.append(t)
            for s in list(S):
                for x in powers:
                    S.add(self.op(x, s))
        return True

    def isAbelian(self):
        """
            Returns true if G is abelian
        """
        if self.abelian != None:
            return self.abelian
        elif self.cyclic:
            self.abelian = True
            return True
        else:
            S = {0}
            for g in range(self.card):
                if g in S:
                    continue
                for s in S:
                    if self.op(s, g) != self.op(g, s):
                        self.abelian = False
                        return False
                powers = [g]
                while True:
                    t = self.op(g, powers[-1])
                    if t == 0 or t in S:
                        break
                    powers.append(t)

                for s in list(S):
                    for x in powers:
                        S.add(self.op(x, s))

            self.abelian = True
        return self.abelian

    def isCyclic(self):
        if self.cyclic == None:
            if isprime(self.card):
                self.cyclic = True
                self.abelian = True
                self.simple = True
                return True
            if not self.isAbelian():
                self.cyclic = False
                return False
            self.cyclic = self.card in self.orders(True)
            return self.cyclic
        return self.cyclic

    def isSimple(self):
        if self.simple != None:
            return self.simple

        if isprime(self.card):
            self.simple = True
            return True
        elif self.card & 1:
            self.simple = False
            return False

        # TODO analize sylow subgroups

        return None

    def isIsomorphic(self, H):
        if repr(self) == repr(H):
            return True
        if self.card != H.card or (self.isAbelian() != H.isAbelian()) or (self.isCyclic() != H.isCyclic()):
            return False
        # TODO

    def __iter__(self):
        return GroupIter(self)

    def __truediv__(self, N):
        from groups import Quotient
        return Quotient(self, N)

    def __mul__(self, H):
        from groups import Direct
        return Direct(self, H)

    def __getitem__(self, i):
        return self.element(i)

    def __eq__(self, H):
        return self.isIsomorphic(H)

class GroupIter():
    def __init__(self, G):
        self.G = G
        self.index = 0

    def __next__(self):
        if self.index < self.G.card:
            g = self.G.element(self.index)
            self.index += 1
            return g
        raise StopIteration()


def cayleyTable(self, truerepr=False):
    """
    truerepr        True prints element name
                    False prints element index
    """
    if truerepr:
        T = [[self[self.op(j, i)] for i in range(self.card)]for j in range(self.card)]
    else:
        T = [[self.op(j, i) for i in range(self.card)]for j in range(self.card)]

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

def composition(f, g):
    return [g[x] for x in f]

class Subgroup(Group):
    def __init__(self, G, gen):
        H = self.__genSubgroup(G, gen)
        self.card = len(H)
        d = {H[i]: i for i in range(len(H))}
        self.element = lambda k: G[H[k]]
        self.index = lambda e: d[G.index(e)]
        self.op = lambda a, b: d[G.op(H[a], H[b])]
        self.abelian = None
        self.cyclic = None
        self.gen = gen
        self.G = G

    def __genSubgroup(self, G, gen):
        H = [0]
        S = {0}
        size = 1

        while True:
            for g in gen:
                for h in H:
                    p = G.op(h, g)
                    if p not in S:
                        H.append(p)
                        S.add(p)
            if size == len(H):
                break
            size = len(H)
        return H

    def __repr__(self):
        return "<"+",".join(str(self.G[g]) for g in self.gen)+">"

class Subset():
    def __init__(self, G, H):
        e = list(H)
        self.element = lambda k: e[k]
        self.card = len(H)
        # This returns an element of G that cannot be converted back to an element of H since we don't know of H is closed under the operation of G
        self.op = lambda g, h: G.op(self.element(g), self.element(h))
        self.subgroup = None

class GroupAction():
    def __init__(self, G, X):
        pass
