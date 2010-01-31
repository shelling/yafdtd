#!/usr/bin/env python
#-*- mode: python -*-

import convention

from fdtd import grid, mesher

# program start

data = numpy.zeros((100,100))
print data

a_plane = grid.Plane(data)
print a_plane
print a_plane.__class__
