#!/usr/bin/env python

import numpy

def combination(shape):
    shape = list(shape)
    index = [[i] for i in range(shape.pop(0))]
    for basis in shape:
        index = [item+[i] for item in index for i in range(basis)]
    return [tuple(item) for item in index]

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
    index = combination(array.shape[1:])
    print timeline(array,index[0])

for array in (a,b,c):
    index = combination(array.shape[1:])
    print array.transpose()[index[0]]

