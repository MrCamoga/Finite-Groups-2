from groups import Direct, Cyclic, Symmetric, Group

def GL32():
    """
        GL(3,2) as subgroup of S8
    """
    H = list()
    det = list()
    C = Direct([Cyclic(2)]*3)
    S = Symmetric(C.card)
    for i in range(1, 2**3):
        for j in range(1, 2**3):
            if j == i:
                continue
            for k in range(1, 2**3):
                if k == i or k == j or k == C.op(i, j):
                    continue
                H.append(S.index(C.automorphism({1: i, 2: j, 4: k})))
                v = [C[a] for a in [i, j, k]]
                det.append((v[0][0]*v[1][1]*v[2][2] + v[0][1]*v[1][2]*v[2][0] + v[1][0]*v[2][1]*v[0][2] - v[2][0]*v[1][1]*v[0][2] - v[1][0]*v[0][1]*v[2][2] - v[2][1]*v[1][2]*v[0][0]) % 2)

    d = {H[i]: i for i in range(len(H))}

    def e(k): return S[H[k]]
    def index(e): return d[S.index(e)]
    def op(g1, g2): return d[S.op(H[g1], H[g2])]

    GL = Group(len(H), e, op)
    GL.index = index

    return GL