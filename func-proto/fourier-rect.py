#!/usr/bin/env python

import numpy
import matplotlib
import pylab

fig = pylab.figure()
fig.hold()
ax = fig.gca()
ax.grid(True)

n = 2**8
t = numpy.linspace(0, 1, n)
y = numpy.zeros(n)

for freq in xrange(1,2000,2):
  y += (4/(numpy.pi*freq))*numpy.sin(2*numpy.pi*freq*t*2)

ax.plot(t,y)
fig.savefig("/tmp/a.png")
