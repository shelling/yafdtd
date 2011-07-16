#!/usr/bin/env python
#-*- mode: python -*-

import sys, os, math, h5py, numpy, pylab
sys.path.append(".")

from yafdtd.source import *
from math import sin, cos, pi


a = numpy.arange(0,20,0.01)
pylab.plot(a, [cos(2*pi*0.5*t)*gaussian(t, 10, 3) for t in a])
pylab.plot(a, [sin(2*pi*0.5*t)*gaussian(t, 10, 3) for t in a])
pylab.show()
