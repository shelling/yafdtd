#!/usr/bin/env python
#-*- mode: python -*-

import sys, os, math, h5py, numpy
sys.path.append(".")

from yafdtd.grid import Plane, PBCPlane, UPMLPlane, XTFSFPlane, DispersivePlane, PolarDPlane
from yafdtd.utils import *
from scipy.constants import c
from math import sin, pi
from yafdtd.geometry import circle

length = 301

plane = DispersivePlane(XTFSFPlane(UPMLPlane(PBCPlane(Plane("silicon-rod-25nm-xtfsf-te-dx1nm", (length,length))))))
plane.open("result/%s/%s.hdf5" % (plane.name, plane.name))
plane.wavelength(347.5*10**-9).dx(10**-9).save_attrs()
plane.pbc(x = False, y = False).pml(thick = 13).set_pml()
plane.teinc.enter = 2
plane.ytfsf = [50,length-50]
plane.xtfsf = [50,length-50]
circle(plane.epsilon_rx, [151,151.5], 25, 12)
circle(plane.epsilon_ry, [151.5,151], 25, 12)
circle(plane.epsilon_rz, [151,151],   25, 12)

prepare("result/%s/ex" % plane.name)
prepare("result/%s/ey" % plane.name)
prepare("result/%s/hz" % plane.name)

for t in range(0,2000):
    plane.t = t
    plane.teinc.update(sin(2*pi*plane.attrs["frequency"]*t*plane.attrs["dt"]))

    plane.update_hpbc()
    plane.update_dfield().update_dtfsf()
    plane.update_efield()

    plane.update_epbc()
    plane.update_bfield().update_btfsf()
    plane.update_hfield()

    plane.save()
    plane.imshow_ex("result/%s/ex/%.4d.png" % (plane.name, t))
    plane.imshow_ey("result/%s/ey/%.4d.png" % (plane.name, t))
    plane.imshow_hz("result/%s/hz/%.4d.png" % (plane.name, t))
    print t

plane.close()
