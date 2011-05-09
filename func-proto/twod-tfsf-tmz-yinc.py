#!/usr/bin/env python
#-*- mode: python -*-

import sys, os, math, h5py, numpy
sys.path.append(".")

from math import sin, pi
from yafdtd.grid import String, Plane, PBCPlane, UPMLPlane, YTFSFPlane, DispersivePlane, PlaneDecorator
from yafdtd.utils import *
from scipy.constants import c, epsilon_0, mu_0

outdir = "result/gold-rod"
prepare(outdir)
hdf5 = h5py.File("result/gold-rod/gold-rod.hdf5", "w")
hdf5.attrs["name"] = "gold-rod"
hdf5.require_group("timeline")

class PolarDPlane(object):
    def __init__(self, shape, a=0, b=0, c=1, d=0, dt=1):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.dt = dt
        self.mask= numpy.zeros(shape)
        self.x   = numpy.zeros(shape)
        self.y   = numpy.zeros(shape)
        self.z   = numpy.zeros(shape)
        self.xp  = numpy.zeros(shape)
        self.yp  = numpy.zeros(shape)
        self.zp  = numpy.zeros(shape)
        self.xp2 = numpy.zeros(shape)
        self.yp2 = numpy.zeros(shape)
        self.zp2 = numpy.zeros(shape)
        return None

    def update(self, plane):
        self.xp2 = self.xp
        self.yp2 = self.yp
        self.zp2 = self.zp
        self.xp = self.x
        self.yp = self.y
        self.zp = self.z
        self.x = self.c1*self.xp + self.c2*self.xp2 + self.c3*plane.exfield
        self.y = self.c1*self.yp + self.c2*self.yp2 + self.c3*plane.eyfield
        self.z = self.c1*self.zp + self.c2*self.zp2 + self.c3*plane.ezfield
        self.x *= self.mask
        self.y *= self.mask
        self.z *= self.mask
        return self

    def set_factor(self):
        denominator = 2*self.d + self.c*self.dt
        self.c1 = (4*self.d - 2*self.b*(self.dt**2)) / denominator
        self.c2 = (-2*self.d + self.c*self.dt) / denominator
        self.c3 = (2*self.a*(self.dt**2)) / denominator
        return None


length = 100
deltat = 3*10**-14
freq = 2*10**12

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

gold = PolarDPlane(plane.shape, a=(9.2*10**13)**2, b=0, c=1.15*10**16, d=1, dt=deltat)
gold.set_factor()
for i in range(0,100):
    for j in range(0,100):
        if math.hypot(i-50,j-50) < 10:
            gold.mask[i,j] = 1



for t in range(0,1000):
    print t
    plane.tminc.update(sin(2*pi*freq*t*deltat))
    # print plane.tminc.inspect()

    plane.update_hpbc()
    plane.update_dfield().update_dtfsf()
    gold.update(plane)
    plane.update_efield(gold)

    plane.update_epbc()
    plane.update_bfield().update_btfsf()
    plane.update_hfield()
    
    # imshow(plane.ezfield, "/tmp/%.3d.png", t)
    hdf5.require_group("timeline/"+str(t))
    hdf5["timeline"][str(t)]["ez"] = plane.ezfield


hdf5.attrs["freq"] = freq
hdf5.attrs["deltat"] = deltat
hdf5.attrs["periodForPhasor"] = 3.0
hdf5.close()



