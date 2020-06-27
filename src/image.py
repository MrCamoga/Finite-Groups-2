from tkinter import PhotoImage, Tk
import colorsys
import group
from random import randint


def saveImage(G,file):
    assert(G.card < 10000)
    window = Tk()
    img = PhotoImage(width=G.card,height=G.card)
    colors = list()
    if len(G) == 1:
        colors = ["#ff0000"]
    else: 
        for k in range(len(G)):
            col = colorsys.hsv_to_rgb(0.833334*k/(len(G)-1),1,1)
            hexcol = "#"+"%02X" % int(col[0]*255)+"%02X" % int(col[1]*255)+"%02X" % int(col[2]*255)
            colors.append(hexcol)

    for i in range(len(G)):
        img.put(" ".join([colors[G.op(j,i)] for j in range(len(G))]), [i,0])

    img.write("cayley tables/"+file+".png",format="png")
    window.destroy()
    
def saveSubset(G,H,file):
    S = list(H)
    D = {S[i]:i for i in range(len(S))}
    
    assert(len(H) < 10000)
    window = Tk()
    img = PhotoImage(width=len(H),height=len(H))
    colors = list()
    if len(H) == 1:
        colors = ["#ff0000"]
    else: 
        for k in range(len(H)):
            col = colorsys.hsv_to_rgb(0.833334*k/(len(H)-1),1,1)
            hexcol = "#"+"%02X" % int(col[0]*255)+"%02X" % int(col[1]*255)+"%02X" % int(col[2]*255)
            colors.append(hexcol)
    
    for i in range(len(H)):
        if i%10==0:
            print(i)
        img.put(" ".join([colors[D[G.op(S[j],S[i])]] for j in range(len(S))]), [i,0])
        
    img.write("cayley tables/"+file+".png",format="png")
    window.destroy()
