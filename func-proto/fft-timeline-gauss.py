#!/usr/bin/env python

import sys, numpy, scipy, matplotlib, pylab
sys.path.append("./lib")
from fdtd.source import gaussian_oft

def fft(t, timedomain, sampleperiod):
    n = len(t)
    f = numpy.arange(-n/2,n/2)/(sampleperiod*n)
    freqdomain = numpy.abs(numpy.fft.fftshift(numpy.fft.fft(timedomain)))
    return f, freqdomain

DEBUG = 0

n = numpy.float(2**18)
freq = 25

dt = 1./800

t = numpy.arange(n)*dt
timedomain = [gaussian_oft(i, 100, 1) for i in t]

f, freqdomain = fft(t, timedomain, dt)

if DEBUG:
  for item in zip(f,freqdomain.round()):
    print item

pylab.subplot(2,1,1)
pylab.plot(t,timedomain)
pylab.xlim(99, 101)

pylab.subplot(2,1,2)
pylab.plot(f,freqdomain)
pylab.xlim(-2,2)

pylab.savefig("/tmp/a.png")
