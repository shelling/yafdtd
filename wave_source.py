#!/usr/bin/env python
#-*- mode: python -*-

import sys
sys.path.append("./lib")

import os
import timeit

import matplotlib
matplotlib.use("Agg")

import numpy
import pylab


from fdtd.source import *

t = numpy.arange(-10, 10, 0.001)
    
pylab.plot(t, map( polynomial_pulse, t ) )
pylab.plot(t, map( polynomial_pulse_p, t ) )
pylab.plot(t, map( polynomial_pulse_pp, t ) )

pylab.xlim(-2, 2)
# pylab.ylim(-0.5, 1.5)
pylab.grid(True)
pylab.savefig("poly.png")
pylab.gcf().clear()
os.system("open poly.png")



one = numpy.ones_like(t)

pylab.plot(t, map( gaussian, t, one*2, one*3 ) )
pylab.plot(t, map( gaussian_p, t, one*2, one*3 ) )

pylab.grid(True)
pylab.savefig("gaussian.png")
pylab.gcf().clear()
os.system("open gaussian.png")
