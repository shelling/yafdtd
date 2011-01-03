#!/usr/bin/env python

import numpy
import scipy
import matplotlib
import pylab

n = numpy.float(2**9)
freq = 25

samplerate = 512
sampletime = 1./samplerate

index = numpy.arange(n)

t = index*sampletime
timedomain = numpy.cos(2*numpy.pi*freq*t)

f = numpy.arange(-n/2,n/2)/(sampletime*n)
freqdomain = numpy.fft.fft(timedomain)

for item in zip(f,numpy.fft.fftshift(numpy.abs(freqdomain).round())):
  print item


pylab.subplot(2,1,1)
pylab.plot(t,timedomain)
pylab.xlim(0, n*sampletime)

pylab.subplot(2,1,2)
pylab.plot(f,numpy.fft.fftshift(numpy.abs(freqdomain)))
# pylab.xlim(-n/2,n/2)

pylab.savefig("/tmp/a.png")

