#!/usr/bin/env python
#-*- mode: python -*-

import convention

from fdtd import source, grid, mesher

pprint(locals())

# program start

p = grid.Plane(numpy.zeros((100,100)))
print(p)
p = mesher.plane(numpy.zeros((10,10)))
print(p)

