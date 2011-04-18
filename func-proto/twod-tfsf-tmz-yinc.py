#!/usr/bin/env python
#-*- mode: python -*-

import sys, os, math, h5py, numpy
sys.path.append(".")

from math import sin, pi
from yafdtd.source import HardSource, TFSF
from yafdtd.grid import String, Plane, PBCPlane, UPMLPlane, PlaneDecorator
from yafdtd.utils import *
from scipy.constants import c, epsilon_0, mu_0

class TFSFPlane(PlaneDecorator):
    def __init__(self, orig):
        super(TFSFPlane, self).__init__(orig)
        self.xinc = String(self.shape[0])
        self.yinc = String(self.shape[1])
        return None
    def update_dtfsf(self):
        self.dzfield[10:21,10] += 0.5 * self.yinc.hfield[10]
        self.dzfield[10:21,20] -= 0.5 * self.yinc.hfield[20]
        return self
    def update_btfsf(self):
        # y edge
        self.bxfield[10:21,9] += 0.5 * self.yinc.dfield[10]
        self.bxfield[10:21,20]-= 0.5 * self.yinc.dfield[20]
        # x edge
        self.byfield[9,10:21] -= 0.5 * self.yinc.dfield[10:21]
        self.byfield[20,10:21]+= 0.5 * self.yinc.dfield[10:21]
        return self

length = 30

plane = Plane((length,length))

plane = PBCPlane(plane)
plane.pbcy = False

plane = UPMLPlane(plane)
plane.pmlx = False
plane.set_pml()

plane = TFSFPlane(plane)
plane.yinc.enter = 2


for t in range(0,100):
    print t
    plane.yinc.update(sin(2*pi*0.01*t))
    print plane.yinc.inspect()

    plane.update_hpbc()
    plane.update_dfield().update_dtfsf()
    plane.update_efield()

    plane.update_epbc()
    plane.update_bfield().update_btfsf()
    plane.update_hfield()
    
    plot(plane.yinc.efield, "/tmp/string-%.3d.png" , t)
    imshow(plane.ezfield, "/tmp/%.3d.png", t)

print plane.inspect()

