import math

def circle(array, center, r, value):
    x,y = array.shape
    for i in range(0,x):
        for j in range(0,y):
            if math.hypot(i-center[0], j-center[1]) <= r:
                array[i,j] = value
    return None

def rectangle(array, center, xlen, ylen, value):
    x,y = array.shape
    for i in range(x):
        for j in range(y):
            if abs(i-center[0]) <= xlen/2 and abs(j-center[1]) <= ylen/2:
                array[i,j] = value
    return None
