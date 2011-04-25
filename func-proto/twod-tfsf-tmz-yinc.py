#!/usr/bin/env python
#-*- mode: python -*-

import sys, os, math, h5py, numpy
sys.path.append(".")

from math import sin, pi
from yafdtd.grid import String, Plane, PBCPlane, UPMLPlane, PlaneDecorator
from yafdtd.utils import *
from scipy.constants import c, epsilon_0, mu_0

class DispersivePlane(PlaneDecorator):
    def __init__(self, orig):
        super(DispersivePlane, self).__init__(orig)
        self.epsilon_r = numpy.ones(self.shape)
        self.mu_r      = numpy.ones(self.shape)
        return None
    def update_efield(self):
        self.exfield = self.dxfield / self.epsilon_r
        self.eyfield = self.dyfield / self.epsilon_r
        self.ezfield = self.dzfield / self.epsilon_r
        return self
    def update_hfield(self):
        self.hxfield = self.bxfield / self.mu_r
        self.hyfield = self.byfield / self.mu_r
        self.hzfield = self.bzfield / self.mu_r
        return self


length = 30

plane = Plane((length,length))

plane = PBCPlane(plane)
plane.pbcy = False

plane = UPMLPlane(plane)
plane.pmlx = False
plane.set_pml()

plane = YTFSFPlane(plane)
plane.tminc.enter = 2
plane.xtfsf = [None, None]

plane = DispersivePlane(plane)
plane.epsilon_r[12:18,12:18] = 12


for t in range(0,100):
    print t
    plane.tminc.update(sin(2*pi*0.01*t))
    print plane.tminc.inspect()

    plane.update_hpbc()
    plane.update_dfield().update_dtfsf()
    plane.update_efield()

    plane.update_epbc()
    plane.update_bfield().update_btfsf()
    plane.update_hfield()
    
    plot(plane.tminc.efield, "/tmp/string-%.3d.png" , t)
    imshow(plane.ezfield, "/tmp/%.3d.png", t)

print plane.inspect()

