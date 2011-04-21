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
        self.dzfield[self.xlow:self.xhigh+1, self.ylow] += 0.5 * self.yinc.hfield[self.ylow]
        self.dzfield[self.xlow:self.xhigh+1, self.yhigh]-= 0.5 * self.yinc.hfield[self.yhigh]
        return self
    def update_btfsf(self):
        # y edge
        self.bxfield[self.xlow:self.xhigh+1, self.ylow-1]+= 0.5 * self.yinc.dfield[self.ylow]
        self.bxfield[self.xlow:self.xhigh+1, self.yhigh] -= 0.5 * self.yinc.dfield[self.yhigh]
        # x edge
        self.byfield[self.xlow-1, self.ylow:self.yhigh+1]-= 0.5 * self.yinc.dfield[self.ylow:self.yhigh+1]
        self.byfield[self.xhigh, self.ylow:self.yhigh+1] += 0.5 * self.yinc.dfield[self.ylow:self.yhigh+1]
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
plane.xlow  = 5
plane.xhigh = 25
plane.ylow  = 8
plane.yhigh = 22


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

