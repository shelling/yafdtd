#!/usr/bin/env python

import sys, numpy, scipy, matplotlib, pylab
sys.path.append(".")
from yafdtd.utils import fft

freq = 10**19
dt = 1./10**20

t = numpy.arange(100)*dt
timedomain = numpy.cos(2*numpy.pi*freq*t)

f = numpy.arange(-50,50)/(dt*100)
freqdomain = numpy.abs(numpy.fft.fftshift(numpy.fft.fft(timedomain)))

pylab.subplot(2,1,1)
pylab.plot(t, timedomain)

pylab.subplot(2,1,2)
pylab.plot(f, freqdomain)

pylab.savefig("/tmp/try.png")
