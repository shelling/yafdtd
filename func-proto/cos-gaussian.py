#!/usr/bin/env python
#-*- mode: python -*-

import sys, os, numpy, pylab
sys.path.append(".")

from yafdtd.source import *
from math import cos, sin, pi

c = 3*10**8

center = 100
dx = 10**-9
dt = dx/(2*c)
freq = 3*10**16

f = dt * freq
print f


time = numpy.arange(201)
g = [cos(2*pi*f*t) for t in time]
pylab.plot(time, g)

g = [gaussian(t, center, 30) for t in time]
pylab.plot(time, g)

g = [cos(2*pi*f*t)*gaussian(t, center, 30) for t in time]
pylab.plot(time, g)

pylab.show()

