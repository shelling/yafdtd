#!/usr/bin/env python
#-*- mode: python -*-

import sys, os, math, h5py, numpy

from yafdtd.source import HardSource, TFSF, sin_oft
from yafdtd.grid import String, Plane, PBCPlane, UPMLPlane
from yafdtd.utils import *
from scipy.constants import c, epsilon_0, mu_0


length = 10

def puts(*things):
    for item in things:
        print item
    return None

String.inspect = (lambda self: puts(self.dfield.round(2), self.efield.round(2), self.bfield.round(2), self.hfield.round(2), ""))
Plane.inspect = (lambda self: puts(self.dzfield.round(2), self.ezfield.round(2), self.bxfield.round(2), self.hxfield.round(2), self.byfield.round(2), self.hyfield.round(2)))

string = String(length)
plane = Plane((length,length))
plane = PBCPlane(plane)


for t in range(0,100):
    print t
    string.dfield[2] = sin_oft(0.005*t)
    string.update_dfield().update_efield().update_abc().update_bfield().update_hfield()
    string.inspect()

    plane.dzfield[3:9,3] += 0.5 * string.hfield[2]
    plane.dzfield[3:9,8] -= 0.5 * string.hfield[8]

    plane.update_hpbc()
    plane.update_dfield()
    plane.update_efield()
    plane.update_epbc()
    plane.update_bfield()
    plane.update_hfield()

    # y edge
    plane.bxfield[3:9,2] += 0.5 * string.dfield[3]
    plane.bxfield[3:9,8] -= 0.5 * string.dfield[8]
    plane.hxfield[3:9,2] += 0.5 * string.efield[3]
    plane.hxfield[3:9,8] -= 0.5 * string.efield[8]


    # x edge
    plane.byfield[2,3:9] -= 0.5 * string.dfield[3:9]
    plane.byfield[8,3:9] += 0.5 * string.dfield[3:9]
    plane.hyfield[2,3:9] -= 0.5 * string.efield[3:9]
    plane.hyfield[8,3:9] += 0.5 * string.efield[3:9]
    
    imshow(plane.ezfield, "/tmp/%.3d.png", t)
plane.inspect()

