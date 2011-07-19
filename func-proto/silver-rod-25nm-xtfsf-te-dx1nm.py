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

plane = DispersivePlane(XTFSFPlane(UPMLPlane(PBCPlane(Plane("silver-rod-25nm-xtfsf-te-dx1nm", (length,length))))))
plane.pml(
    thick = 13
)
plane.pbc(
    x = False,
    y = False
)
plane.tfsf(
    xtfsf = [50, length-50],
    ytfsf = [50, length-50],
    enter = 2
)
plane.circle_e([151,151], 25, 8.926)
plane.open("result/%s/%s.hdf5" % (plane.name, plane.name))
plane.wavelength(347.5*10**-9).dx(10**-9).save_attrs()

# metal = PolarDPlane(plane.shape, a=(9.39*10**15)**2, b=0, c=3.14*10**13, d=1, dt=plane.attrs["dt"])
metal = PolarDPlane(plane.shape, a=(1.757*10**16)**2, b=0, c=3.0786*10**14, d=1, dt=plane.attrs["dt"])
metal.set_factor()
metal.circle([151,151], 25, 1)

prepare("result/%s/ex" % plane.name)
prepare("result/%s/ey" % plane.name)
prepare("result/%s/hz" % plane.name)

for t in range(0,4500):
    plane.t = t
    plane.teinc.update(sin(2*pi*plane.attrs["frequency"]*t*plane.attrs["dt"]))

    plane.update_hpbc()
    plane.update_dfield().update_dtfsf()
    metal.update(plane)
    plane.update_efield(metal)

    plane.update_epbc()
    plane.update_bfield().update_btfsf()
    plane.update_hfield()

    plane.save()
    plane.imshow_ex("result/%s/ex/%.4d.png" % (plane.name, t))
    plane.imshow_ey("result/%s/ey/%.4d.png" % (plane.name, t))
    plane.imshow_hz("result/%s/hz/%.4d.png" % (plane.name, t))
    print t

plane.close()
