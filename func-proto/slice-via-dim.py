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

def timeline(timeline, coordinates):
    for basis in range(len(coordinates)):
        timeline = timeline[:,coordinates[basis]]
    return timeline

a = numpy.arange(0,100)
b = numpy.arange(0,1000)
c = numpy.arange(0,10000)

a.shape = (10,10,)
b.shape = (10,10,10)
c.shape = (10,10,10,10)
#           t  x  y  z

for array in (a,b,c):
    index = combination(array.shape)
    print timeline(array,index[0])

