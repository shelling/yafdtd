#!/usr/bin/env python
#-*- mode: python -*-

import convention
import math
import os, csv, re

from fdtd import source
from fdtd.algorithm.onedim import *

efield = numpy.zeros(31)
hfield = numpy.zeros(31)


efield_lm1 = 0
efield_lm2 = 0
efield_rm1 = 0
efield_rm2 = 0

for t in range(1,140):

    update_efield(efield, hfield)

    efield[0]  = efield_lm2
    efield_lm2 = efield_lm1
    efield_lm1 = efield[1]

    efield[efield.shape[0]-1] = efield_rm2
    efield_rm2 = efield_rm1
    efield_rm1 = efield[efield.shape[0]-2]

    
    xcenter = efield.shape[0]/2
    efield[xcenter] = source.gaussian_oft(t, 20, 5)

    
    update_hfield(efield, hfield)

    pylab.grid(True)
    pylab.plot( efield )
    pylab.ylim([-1,1])
    pylab.savefig("result/oned-testing-%.3d.png" % t)
    pylab.clf()
    print t



if "Darwin" in os.uname():
    os.system("open result")
