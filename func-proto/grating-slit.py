#!/usr/bin/env python
#-*- mode: python -*-

import sys, os
sys.path.append(".")

from yafdtd.grid import Plane, PBCPlane, UPMLPlane, XTFSFPlane, DispersivePlane, PolarDPlane
from yafdtd.source import gaussian
from yafdtd.utils import *
from scipy.constants import c
from math import pi, sin, cos
from sys import stdout


plane = DispersivePlane(XTFSFPlane(UPMLPlane(PBCPlane(Plane("grating-slit", (301,701))))))
plane.dx(10**-9).wavelength(347.5*10**-9)

plane.pml( 
    x = True,
    y = False,
    thick = 20 
).set_pml()

plane.pbc( 
    x = False,
    y = True 
)

plane.tfsf(
    xtfsf = [50, 301-50],
    ytfsf = [None, None],
    enter = 2
)

for t in range(0,1200):
    stdout.write("\b\b\b\b%d"%t)
    plane.t = t
    plane.teinc.update(cos(2*pi*0.025*t)*gaussian(t, 200, 60))

    pylab.plot(plane.teinc.efield)
    pylab.ylim(-1,1)
    pylab.savefig("/tmp/teinc-%.3d.png"%t)
    pylab.clf()

    plane.update_hpbc()
    plane.update_dfield().update_dtfsf()
    plane.update_efield()

    plane.update_epbc()
    plane.update_bfield().update_btfsf()
    plane.update_hfield()

    plane.imshow_hz("/tmp/grating-slit%.4d.png"%t)
