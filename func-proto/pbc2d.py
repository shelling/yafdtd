#!/usr/bin/env python
#-*- mode: python -*-

import os, sys, numpy, pylab
sys.path.append(".")

from yafdtd.grid import Plane, PBCPlane, UPMLPlane
from yafdtd.utils import *
from scipy.constants import c
from math import sin, pi
from yafdtd.geometry import circle


deltax = 10**-9
deltat = deltax/(2*c)
freq   = 4*10**15


plane = PBCPlane(Plane("pbc2d", (900,900)))
plane.pbc(x=True, y=True)

for t in range(300):
    print t

    plane.update_hpbc()
    plane.update_dfield()
    plane.update_efield()

    plane.ezfield[15,15] = sin(2*pi*freq*t*deltat)

    plane.update_epbc()
    plane.update_bfield()
    plane.update_hfield()

    # plane.imshow_ez("/tmp/pbc-ez-%.3d.png"%t)
