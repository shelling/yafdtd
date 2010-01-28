#!/usr/bin/env python
#-*- mode: python -*-

from convention import *
import_convention(globals())

from pylab import *
from mpmath import *


# program start
data = numpy.zeros((50,50))

for i in range(0,50):
    for j in range(0,50):
        coefficient = pi/mpf(12.25)
        data[i,j] = sin(i*coefficient) * sin(j*coefficient)


imshow(data)
colorbar()
savefig("show_img.png")
clf()
os.system("open show_img.png")


# plot grid.Plane
from fdtd import grid
plane = grid.Plane(data)

imshow(numpy.array(plane,dtype="float"))
colorbar()
savefig("plane.png")
clf()
os.system("open plane.png")

