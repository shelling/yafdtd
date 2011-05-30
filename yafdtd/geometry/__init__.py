import math

def circle(plane, center, r, value):
    x,y = plane.shape
    for i in range(0,x):
        for j in range(0,y):
            if math.hypot(i-center[0], j-center[1]) <= r:
                plane[i,j] = value
    return None
