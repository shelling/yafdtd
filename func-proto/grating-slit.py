#!/usr/bin/env python
#-*- mode: python -*-

import sys, os
sys.path.append(".")

from yafdtd.grid import Plane, PBCPlane, UPMLPlane, XTFSFPlane, DispersivePlane, PolarDPlane
from yafdtd.source import gaussian
from yafdtd.utils import *
from scipy.constants import c
from math import pi, sin, cos
from sys import stdout


plane = DispersivePlane(XTFSFPlane(UPMLPlane(PBCPlane(Plane("grating-slit", (301,701))))))

plane.pml( 
    x = True,
    y = False,
    thick = 20 
).pbc( 
    x = False,
    y = True 
).tfsf(
    xtfsf = [50, 301-50],
    ytfsf = [None, None],
    enter = 2
).open(
    "result/grating-slit/result.hdf5"
).dx(
    5e-9
).frequency(
    # 1.5e14
    6e14
).save_attrs()

plane.rectangle_e(center=[151,351], xlen=70, ylen=710, value=8.9)
plane.rectangle_e(center=[151,351], xlen=70, ylen=8,   value=1)
plane.rectangle_e(center=[126,251], xlen=20, ylen=8,   value=1)
plane.rectangle_e(center=[126,451], xlen=20, ylen=8,   value=1)
plane.rectangle_e(center=[126,151], xlen=20, ylen=8,   value=1)
plane.rectangle_e(center=[126,551], xlen=20, ylen=8,   value=1)


metal = PolarDPlane(plane.shape, a=(1.757*10**16)**2, b=0, c=3.0786*10**14, d=1, dt=plane.dt()).set_factor()
metal.rectangle(center=[151,351], xlen=70, ylen=710, value=1)
metal.rectangle(center=[151,351], xlen=70, ylen=8,   value=0)
metal.rectangle(center=[126,251], xlen=20, ylen=8,   value=0)
metal.rectangle(center=[126,451], xlen=20, ylen=8,   value=0)
metal.rectangle(center=[126,151], xlen=20, ylen=8,   value=0)
metal.rectangle(center=[126,551], xlen=20, ylen=8,   value=0)

dt = plane.dt()
freq = plane.frequency()

for t in range(0,7000):
    stdout.write("\b\b\b\b%d"%t)
    plane.t = t

    plane.teinc.update(cos(2*pi*freq*t*dt)*gaussian(t*dt, 800*dt, 150*dt))#.plot_e("result/grating-slit/teinc/teinc-%.4d.png"%t)

    plane.update_dfield().update_dtfsf()
    metal.update(plane)
    plane.update_efield(metal).update_epbc()

    plane.update_bfield().update_btfsf()
    plane.update_hfield().update_hpbc()

    plane.imshow_hz("result/grating-slit/hz/grating-slit-%.4d.png"%t)
    plane.save()

