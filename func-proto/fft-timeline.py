#!/usr/bin/env python

import sys, numpy, scipy, matplotlib, pylab
sys.path.append(".")
from yafdtd.source import gaussian
from yafdtd.utils  import fft
from math import pi, sin, cos

DEBUG = 0

n = numpy.float(2**10)
freq = 25

dt = 1./1024

t = numpy.arange(n)*dt
timedomain = numpy.cos(2*numpy.pi*freq*t)

f, freqdomain = fft(t, timedomain, dt)

if DEBUG:
  for item in zip(f,freqdomain.round()):
    print item

pylab.subplot(2,2,1)
pylab.plot(t,timedomain)
pylab.xlim(0, n*dt)

pylab.subplot(2,2,3)
pylab.plot(f,freqdomain)
pylab.xlim(-n/2,n/2)


n = numpy.float(2**18)

dt = 1./1024

t = numpy.arange(n)*dt
timedomain = [cos(2*pi*5*i)*gaussian(i, 100, 0.25) for i in t]

f, freqdomain = fft(t, timedomain, dt)

if DEBUG:
  for item in zip(f,freqdomain.round()):
    print item

pylab.subplot(2,2,2)
pylab.plot(t,timedomain)
pylab.xlim(99, 101)

pylab.subplot(2,2,4)
pylab.plot(f,freqdomain)
pylab.xlim(-10,10)

pylab.savefig("/tmp/a.png")

