#Rubik's Cube

from groups import GeneralizedSymmetric
from functools import reduce

def Rubik222():
    """
        The elements operate in the usual order. Example: RUR'U' = G.op(R,U,R,R,R,U,U,U)
        Returns G, (R,U,F,L,D,B)
    """
    G = GeneralizedSymmetric(3,8)

    return (G, (19106868, 38578680, 133254322, 105367583, 118098, 3212037))
    
def Rubik333():
    """
        The elements operate in the usual order. Example: RUR'U' = G.op(R,U,R,R,R,U,U,U)
        Returns G, (R,U,F,L,D,B,M,E,S,X,Y,Z)
    """
    G = GeneralizedSymmetric(3,8)*GeneralizedSymmetric(2,12)

    return (G, ((12260357905730210868, 47577203601977420280, 307133848437835100722, 137967831317727263, 19503969848658, 1232685858040989957, 93631695786114433920, 16383398063155200, 8613117329516824320, 361990033464047119142, 47583584714230479009, 316877050992623394868)))
