#!/usr/bin/env python
#-*- mode: python -*-

import sys, os, numpy, pylab
sys.path.append(".")

from yafdtd.source import *
from yafdtd.utils import fft
from math import cos, sin, pi

c = 3*10**8

center = 5000
width = 600

dx = 10**-9
dt = dx/(2*c)
freq = c/200e-9

print freq


pylab.subplot(2,1,1)

time = numpy.arange(20001)
g = [cos(2*pi*freq*t*dt) for t in time]
pylab.plot(time, g)

g = [gaussian(t*dt, center*dt, width*dt) for t in time] # timing dt isn't necessary due to perfect scaling
pylab.plot(time, g)

g = [cos(2*pi*freq*t*dt)*gaussian(t*dt, center*dt, width*dt) for t in time]
pylab.plot(time, g)



pylab.subplot(2,1,2)

freq, spectrum = fft(time, g, dt)
pylab.plot(freq, spectrum)
pylab.xlim(0,4e15)

pylab.show()

