from groups import Group, Direct, Cyclic, Symmetric

def GL23():
    """
        GL(2,3) as subgroup of S9
    """
    H = list()
    det = list()
    C = Direct([Cyclic(3)]*2)
    S = Symmetric(C.card)
    for i in range(1, 3**2):
        for j in range(1, 3**2):
            if j == i or j == C.op(i, i):
                continue
            H.append(S.index(C.automorphism({1: i, 3: j})))
            v = [C[a] for a in [i, j]]
            det.append((v[0][0]*v[1][1]-v[1][0]*v[0][1]) % 3)

    d = {H[i]: i for i in range(len(H))}

    def e(k): return S[H[k]]
    def index(e): return d[S.index(e)]
    def op(g1, g2): return d[S.op(H[g1], H[g2])]

    GL = Group(len(H), e, op)
    GL.index = index

    return GL