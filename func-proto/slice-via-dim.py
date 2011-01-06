#!/usr/bin/env python

import numpy

def combination(shape):
    shape = list(shape)
    while len(shape) < 4:
        shape.append(None)
    (t,x,y,z) = shape
    index = [[i] for i in range(x)]
    index = [item+[j] for item in index for j in range(y)] if y else index
    index = [item+[k] for item in index for k in range(z)] if z else index
    return index

a = numpy.arange(0,1000)
a.shape = (10,10,10,)
#           t  x  y  z

index = combination(a.shape)

# index = [tuple(item) for item in index]

print a[:,0,0]
print index[0]
while len(index[0]) < 3:
    index[0].append(None)
index[0] = tuple(index[0])
print index[0]
print a[:,0,0,None].flatten()


