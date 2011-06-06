#!/usr/bin/env python
#-*- mode: python -*-

import sys, os, math, h5py, numpy
sys.path.append(".")

from math import sin, pi
from yafdtd.grid import Plane, PBCPlane, UPMLPlane, YTFSFPlane, DispersivePlane, PolarDPlane
from yafdtd.utils import *
from yafdtd.geometry import circle
from scipy.constants import c, epsilon_0, mu_0

name = "silver-rod"
outdir = "result/%s" % name
prepare(outdir)
hdf5 = h5py.File("%s/%s.hdf5" % (outdir, name), "w")
hdf5.attrs["name"] = name 
hdf5.require_group("timeline")

length = 301
deltax = 10**-9
deltat = deltax/(2*c)
freq   = 5*10**14

plane = DispersivePlane(YTFSFPlane(UPMLPlane(PBCPlane(Plane((length,length))))))

plane.pbcx = False
plane.pbcy = False
# plane.pmly = False
plane.pml_thick = 10
plane.set_pml()
plane.tminc.enter = 2
plane.xtfsf = [50,251]
plane.ytfsf = [50,251]

metal = PolarDPlane(plane.shape, a=(9.39*10**15)**2, b=0, c=3.14*10**13, d=1, dt=deltat)
metal.set_factor()
circle(metal.mask, [121,151], 25, 1)
circle(metal.mask, [181,151], 25, 1)

for t in range(0,2000):
    plane.tminc.update(sin(2*pi*freq*t*deltat))

    plane.update_hpbc()
    plane.update_dfield().update_dtfsf()
    metal.update(plane)
    plane.update_efield(metal)

    plane.update_epbc()
    plane.update_bfield().update_btfsf()
    plane.update_hfield()
    
    hdf5.require_group("timeline/"+str(t))
    hdf5["timeline"][str(t)]["ez"] = plane.ezfield
    print t

hdf5.attrs["freq"] = freq
hdf5.attrs["deltat"] = deltat
hdf5.close()
