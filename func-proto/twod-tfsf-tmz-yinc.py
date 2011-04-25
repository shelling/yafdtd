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

class YTFSFPlane(PlaneDecorator):
    def __init__(self, orig):
        super(YTFSFPlane, self).__init__(orig)
        self.tminc = String(self.shape[1])
        self.teinc = String(self.shape[1])
        self.xtfsf = [10, self.shape[0]-10]
        self.ytfsf = [10, self.shape[1]-10]
        return None
    def update_dtfsf(self):
        if self.xtfsf == [None, None]:
            self.dzfield[:, self.ytfsf[0]]  += 0.5 * self.tminc.hfield[self.ytfsf[0]]
            self.dzfield[:, self.ytfsf[1]]  -= 0.5 * self.tminc.hfield[self.ytfsf[1]]
        else:
            self.dzfield[self.xtfsf[0]:self.xtfsf[1]+1, self.ytfsf[0]]  += 0.5 * self.tminc.hfield[self.ytfsf[0]]
            self.dzfield[self.xtfsf[0]:self.xtfsf[1]+1, self.ytfsf[1]]  -= 0.5 * self.tminc.hfield[self.ytfsf[1]]
        return self
    def update_btfsf(self):
        if self.xtfsf == [None, None]:
            # y edge
            self.bxfield[:, self.ytfsf[0]-1]+= 0.5 * self.tminc.dfield[self.ytfsf[0]]
            self.bxfield[:, self.ytfsf[1]]  -= 0.5 * self.tminc.dfield[self.ytfsf[1]]
        else:
            # y edge
            self.bxfield[self.xtfsf[0]:self.xtfsf[1]+1, self.ytfsf[0]-1] += 0.5 * self.tminc.dfield[self.ytfsf[0]]
            self.bxfield[self.xtfsf[0]:self.xtfsf[1]+1, self.ytfsf[1]]   -= 0.5 * self.tminc.dfield[self.ytfsf[1]]
            # x edge
            self.byfield[self.xtfsf[0]-1, self.ytfsf[0]:self.ytfsf[1]+1] -= 0.5 * self.tminc.dfield[self.ytfsf[0]:self.ytfsf[1]+1]
            self.byfield[self.xtfsf[1],   self.ytfsf[0]:self.ytfsf[1]+1] += 0.5 * self.tminc.dfield[self.ytfsf[0]:self.ytfsf[1]+1]
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

