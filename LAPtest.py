from PIL import Image
from functools import partial
from Matrix import *

LAP = Matrix(((0,1,0),(1,-4,1),(0,1,0)))
LAPB = Matrix(((0,-1,0),(-1,4,-1),(0,-1,0)))

def IMLAP(x, alpha = 0.5):
    if x.mode == 'L':
        n, m = x.size
        xM = Matrix(tuple(tuple(x.load()[i, j] for i in range(n)) for j in range(m)))
        yM = xM.convolution(LAP)
        y = Image.new('L', x.size)
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                y.putpixel((i - 1, j - 1), xM[j - 1][i - 1] - yM[j][i] * alpha)
        return y
    elif x.mode == 'RGB':
        return Image.merge('RGB', tuple(map(partial(IMLAP, alpha = alpha), x.split())))