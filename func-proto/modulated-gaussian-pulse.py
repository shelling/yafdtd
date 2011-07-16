#!/usr/bin/env python
#-*- mode: python -*-

import sys, os, math, h5py, numpy, pylab
sys.path.append(".")

from yafdtd.source import *
from yafdtd.utils import fft
from math import sin, cos, pi


time = numpy.arange(0,20,0.01)

no_module = [gaussian(t, 10, 3) for t in time]
pylab.subplot(2,2,1)
pylab.plot(time, no_module)

cos_module = [cos(2*pi*0.5*t)*gaussian(t, 10, 3) for t in time]
sin_module = [sin(2*pi*0.5*t)*gaussian(t, 10, 3) for t in time]
pylab.subplot(2,2,2)
pylab.plot(time, cos_module)
pylab.plot(time, sin_module)

pylab.subplot(2,2,3)
freq, no_module_spec = fft(time, no_module, 0.01)
pylab.plot(freq[990:1010], no_module_spec[990:1010])

pylab.subplot(2,2,4)
freq, cos_module_spec = fft(time, cos_module, 0.01)
freq, sin_module_spec = fft(time, sin_module, 0.01)
pylab.plot(freq[980:1020], cos_module_spec[980:1020])
pylab.plot(freq[980:1020], sin_module_spec[980:1020])


pylab.show()


