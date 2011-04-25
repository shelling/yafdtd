#!/usr/bin/env python
#-*- mode: python -*-

import sys, os, math, h5py, numpy
sys.path.append(".")

from math import sin, pi
from yafdtd.grid import String, Plane, PBCPlane, UPMLPlane, YTFSFPlane, PlaneDecorator
from yafdtd.utils import *
from scipy.constants import c, epsilon_0, mu_0

class PolarDPlane(object):
    def __init__(self, shape):
        self.x = numpy.zeros(shape)
        self.y = numpy.zeros(shape)
        self.z = numpy.zeros(shape)
        self.xp = numpy.zeros(shape)
        self.yp = numpy.zeros(shape)
        self.zp = numpy.zeros(shape)
        return None
    def update(self, plane):
        return self

class DispersivePlane(PlaneDecorator):
    def __init__(self, orig):
        super(DispersivePlane, self).__init__(orig)
        self.epsilon_r = numpy.ones(self.shape)
        self.mu_r      = numpy.ones(self.shape)
        return None
    def update_efield(self, *polar):
        self.exfield  = self.dxfield.copy()
        self.eyfield  = self.dyfield.copy()
        self.ezfield  = self.dzfield.copy()
        for p in polar:
            self.exfield += polar.x
            self.eyfield += polar.y
            self.ezfield += polar.z
        self.exfield /= self.epsilon_r
        self.eyfield /= self.epsilon_r
        self.ezfield /= self.epsilon_r
        return self
    def update_hfield(self, *polar):
        self.hxfield  = self.bxfield.copy()
        self.hyfield  = self.byfield.copy()
        self.hzfield  = self.bzfield.copy()
        for p in polar:
            self.hxfield += polar.x
            self.hyfield += polar.y
            self.hzfield += polar.z
        self.hxfield /= self.mu_r
        self.hyfield /= self.mu_r
        self.hzfield /= self.mu_r
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
plane.epsilon_r[13:17,13:17] = 12


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

