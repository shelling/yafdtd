#!/usr/bin/env python
#-*- mode: python -*-

import sys, matplotlib
sys.path.append("lib")
matplotlib.use("Agg")

import os, pylab, scipy


from yafdtd.source import *

# program start
t = numpy.arange(-10, 10, 0.01)        # x axis range

# plot polynomial
pylab.plot(t, map( polynomial_pulse, t ) )
pylab.plot(t, map( polynomial_pulse_p, t ) )
pylab.plot(t, map( polynomial_pulse_pp, t ) )

pylab.xlim(-2, 2)
pylab.grid(True)
pylab.savefig("poly.png")
pylab.clf()
# os.system("open poly.png")

# plot gaussian
one = numpy.ones_like(t)

pylab.plot(t, [ gaussian(x,2,3) for x in t ])
pylab.plot(t, [ gaussian_p(x,2,3,) for x in t ])

pylab.grid(True)
pylab.savefig("gaussian.png")
pylab.clf()
# os.system("open gaussian.png")

# simple fourier transform a step function
s = numpy.zeros(1000)
s[:100] = 1
pylab.plot(s)
pylab.plot(scipy.fft(s))
pylab.grid(True)
pylab.savefig("simple_fft.png")
pylab.clf()
# os.system("open simple_fft.png")

# plot fourier transform of gaussian

g = numpy.array([ gaussian(x,2,3) for x in t ], dtype="float")

pylab.plot(t, scipy.fft(g))

pylab.savefig("gaussian_p_fft.png")
# os.system("open gaussian_p_fft.png")
