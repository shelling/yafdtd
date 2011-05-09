#!/usr/bin/env python
#-*- mode: python -*-

import sys, numpy, scipy, matplotlib, pylab
sys.path.append(".")
from numpy.fft import fftshift, fft
from numpy import abs

freq = 100
dt = 1./10000

t = numpy.arange(10)*dt
timedomain = numpy.cos(2*numpy.pi*freq*t)

f = numpy.arange(-5,5)/(dt*10)
freqdomain = abs(fftshift(fft(timedomain)))/10

pylab.subplot(2,1,1)
pylab.plot(t, timedomain)
pylab.subplot(2,1,2)
pylab.plot(f, freqdomain)
pylab.savefig("/tmp/fft-twod-timeline.png")

####################

t2d = numpy.float64(numpy.mgrid[:10,:2,:2][0])*dt

timedomain2d = numpy.cos(2*numpy.pi*freq*t2d)
timedomain2d[:,0,1] = 1
timedomain2d[:,1,0] = 2
timedomain2d[:,1,1] = 3

freqdomain2d = fftshift(abs(fft(timedomain2d, axis=0)), axes=(0,))/10

print freqdomain
print freqdomain2d[:,0,0]/freqdomain

print freqdomain2d

pylab.clf()
pylab.subplot(2,1,1)
pylab.plot(t2d[:,0,0], timedomain2d[:,0,0])
pylab.subplot(2,1,2)
pylab.plot(f, freqdomain2d[:,0,0])
pylab.savefig("/tmp/fft2d.png")
