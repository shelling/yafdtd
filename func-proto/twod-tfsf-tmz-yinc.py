#!/usr/bin/env python
#-*- mode: python -*-

import sys, os, math, h5py, numpy
sys.path.append(".")

from math import sin, pi
from yafdtd.source import HardSource, TFSF
from yafdtd.grid import String, Plane, PBCPlane, UPMLPlane, PlaneDecorator
from yafdtd.utils import *
from scipy.constants import c, epsilon_0, mu_0


length = 30

string = String(length)
string.enter = 2
plane = Plane((length,length))
plane = PBCPlane(plane)
plane.pbcy = False
plane = UPMLPlane(plane)
plane.pmlx = False
plane.set_pml()


for t in range(0,100):
    print t
    string.update(sin(2*pi*0.01*t))
    print string.inspect()

    plane.update_hpbc()
    plane.update_dfield()

    plane.dzfield[10:21,10] += 0.5 * string.hfield[10]
    plane.dzfield[10:21,20] -= 0.5 * string.hfield[20]

    plane.update_efield()
    plane.update_epbc()
    plane.update_bfield()

    # y edge
    plane.bxfield[10:21,9] += 0.5 * string.dfield[10]
    plane.bxfield[10:21,20] -= 0.5 * string.dfield[20]
    # x edge
    plane.byfield[9,10:21] -= 0.5 * string.dfield[10:21]
    plane.byfield[20,10:21] += 0.5 * string.dfield[10:21]

    plane.update_hfield()
    
    plot(string.efield, "/tmp/string-%.3d.png" , t)
    imshow(plane.ezfield, "/tmp/%.3d.png", t)

print plane.inspect()

