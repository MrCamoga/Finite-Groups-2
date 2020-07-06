import png
import colorsys

def iter_rows(G):
    colors = list()
    if len(G) == 1:
        colors = [[255,0,0]]
    else:
        numhues = min(len(G)-1,800)
        for k in G:
            color = colorsys.hsv_to_rgb(5/6*k/numhues % 1,1,1-(k//numhues)*0.01)
            colors[k] = [int(color[i]*255) for i in range(3)]
    
    for i in G:
        row = [0]*3*len(G)
        for j in G:
            p = G.op(i,j)
            row[3*j] = colors[p][0]
            row[3*j+1] = colors[p][1]
            row[3*j+2] = colors[p][2]
        print(i)
        yield row

def saveImage(G,file):
    assert(G.card < 20000)
    
    png.from_array(iter_rows(G), 'RGB', {'width': len(G), 'height': len(G)}).save(file)
