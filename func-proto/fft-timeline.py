#!/usr/bin/env python

import numpy
import scipy
import matplotlib
import pylab

n = numpy.float(2**9)
freq = 25

t = numpy.arange(n)/n
timedomain = numpy.cos(2*numpy.pi*freq*t)

f = t*n
freqdomain = numpy.fft.fft(timedomain)

for item in zip(f,numpy.abs(freqdomain.round())):
  print item

pylab.subplot(2,1,1)
pylab.plot(t,timedomain)

pylab.subplot(2,1,2)
pylab.plot(f-n/2,numpy.fft.fftshift(numpy.abs(freqdomain)))
pylab.xlim(-n/2,n/2)

pylab.savefig("/tmp/a.png")

