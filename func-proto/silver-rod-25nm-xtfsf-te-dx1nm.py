#!/usr/bin/env python
#-*- mode: python -*-

import sys, os, math, h5py, numpy
sys.path.append(".")

from yafdtd.grid import Plane, PBCPlane, UPMLPlane, XTFSFPlane, DispersivePlane, PolarDPlane
from yafdtd.grid import String
from yafdtd.utils import *
from scipy.constants import c, epsilon_0, mu_0
from math import sin, pi
from yafdtd.geometry import circle

name = "silver-rod-25nm-xtfsf-te-dx1nm"
outdir = "result/%s" % name
prepare(outdir)
hdf5 = h5py.File("%s/%s.hdf5" % (outdir, name), "w")
hdf5.attrs["name"] = name 
hdf5.require_group("timeline")

length = 301
deltax = 10**-9
deltat = deltax/(2*c)
freq   = 8.63*10**14

hdf5.attrs["freq"] = freq
hdf5.attrs["deltat"] = deltat

plane = DispersivePlane(XTFSFPlane(UPMLPlane(PBCPlane(Plane((length,length))))))
plane.pbcx = False
plane.pbcy = False
# plane.pmly = False
plane.pml_thick = 13
plane.set_pml()
plane.teinc.enter = 2
plane.ytfsf = [25,length-25]
plane.xtfsf = [25,length-25]

metal = PolarDPlane(plane.shape, a=(9.39*10**15)**2, b=0, c=3.14*10**13, d=1, dt=deltat)
metal.set_factor()
circle(metal.mask, [151,151], 25, 1)

for t in range(0,2000):
    plane.teinc.update(sin(2*pi*freq*t*deltat))

    plane.update_hpbc()
    plane.update_dfield().update_dtfsf()
    metal.update(plane)
    plane.update_efield(metal)

    plane.update_epbc()
    plane.update_bfield().update_btfsf()
    plane.update_hfield()

    hdf5.require_group("timeline/"+str(t))
    hdf5["timeline"][str(t)]["ez"] = plane.hzfield
    print t

hdf5.close()
