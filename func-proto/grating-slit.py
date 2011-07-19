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


plane = DispersivePlane(XTFSFPlane(UPMLPlane(PBCPlane(Plane("grating-slit", (301,301))))))

plane.pml( 
    x = True,
    y = False,
    thick = 20 
)

plane.pbc( 
    x = False,
    y = True 
)

plane.tfsf(
    xtfsf = [50, 301-50],
    ytfsf = [None, None],
    enter = 2
)

plane.open("result/grating-slit/result.hdf5")
plane.dx(10**-9).wavelength(200e-9).save_attrs()
# plane.rectangle_e(center=[151,151], xlen=40, ylen=80, value=12)
plane.circle_e(center=[151,151], r=25, value=12)

metal = PolarDPlane(plane.shape, a=(1.757*10**16)**2, b=0, c=3.0786*10**14, d=1, dt=plane.attrs["dt"])
metal.set_factor()
metal.circle([151,151], 25)


dt = plane.attrs["dt"]
freq = plane.attrs["frequency"]


for t in range(0,10000):
    stdout.write("\b\b\b\b%d"%t)
    plane.t = t

    # plane.teinc.update(cos(2*pi*freq*t*dt)*gaussian(t*dt, 800*dt, 250*dt))
    plane.teinc.update(sin(2*pi*freq*t*dt))
    plane.teinc.plot_e("/tmp/teinc/teinc-%.4d.png"%t)

    plane.update_hpbc()
    plane.update_dfield().update_dtfsf()
    metal.update(plane)
    plane.update_efield(metal)

    plane.update_epbc()
    plane.update_bfield().update_btfsf()
    plane.update_hfield()


    plane.imshow_hz("/tmp/grating-slit/grating-slit%.4d.png"%t)
