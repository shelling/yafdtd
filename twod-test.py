#!/usr/bin/env python
#-*- mode: python -*-
import convention
import os, csv, re

from fdtd import source
from fdtd.algorithm.twodim.freespace import *
from fdtd.grid import Plane

plane = Plane( (31,31), "TM")

for t in range(0,40):
    update_efield( plane )
    plane.ezfield[plane.shape[0]/2, plane.shape[1]/2] = source.gaussian_oft(t, 5, 5)
    update_hfield( plane )
    
    pylab.imshow( plane.ezfield, norm=matplotlib.colors.Normalize(-1,1,True) )
    pylab.colorbar()
    pylab.savefig("result/twod-testing-%.3d.png" % t)
    pylab.clf()
    print t
