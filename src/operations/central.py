from groups import Group

def CentralProduct(A: Group, B: Group, C: list, D: list, f: list):
    """
        Central product of two groups A and B with C and D central subgroups of A and B respectively
        is the quotient of AxB by the subgroup {(g,f-1(g)) : g∈A } and f : C -> D is an isomorphism
        A and B are Groups
        C and D are lists of subgroups
        f is the isomorphism between the centers C and D viewed as a permutation. Example: f = [0,3,2,1]
    """
    assert(set(C).issubset(A.center())) # TODO optimize Group.isCentral(set)
    assert(set(D).issubset(B.center()))
    assert(len(C) == len(D) and len(C) == len(f))
    # TODO verify f is an isomorphism

    AB = A*B
    Z = {AB.indexe((C[g], B.inverse(D[f[g]]))) for g in C}

    return AB/Z