#!/usr/bin/env python
#-*- mode: python -*-

import sys, os, math, h5py, numpy
sys.path.append(".")

from math import sin, pi
from yafdtd.grid import Plane, PBCPlane, UPMLPlane, YTFSFPlane, DispersivePlane, PolarDPlane
from yafdtd.utils import *
from scipy.constants import c, epsilon_0, mu_0

name = "silver-bulk"
outdir = "result/%s" % name
prepare(outdir)
hdf5 = h5py.File("result/%s/%s.hdf5" % (name, name), "w")
hdf5.attrs["name"] = name
hdf5.require_group("timeline")

length = 201
deltax = 10**(-9)
deltat = deltax/(2*c)
freq   = 5*10**14

plane = DispersivePlane(YTFSFPlane(UPMLPlane(PBCPlane(Plane((length,length))))))
plane.pbcy = False
plane.pmlx = False
plane.pml_thick = 20
plane.set_pml()
plane.tminc.enter = 2
plane.xtfsf = [None, None]
plane.ytfsf = [25,176]

# metal = PolarDPlane(plane.shape, a=(1.25663*10**16)**2, b=0, c=5.7*10**13, d=1, dt=deltat)
metal = PolarDPlane(plane.shape, a=(9.39*10**15)**2, b=0, c=3.14*10**13, d=1, dt=deltat)
metal.set_factor()
metal.mask[:,50:80] = 1

for t in range(0,3000):
    print t
    plane.tminc.update(sin(2*pi*freq*t*deltat))
    # print plane.tminc.inspect()

    plane.update_hpbc()
    plane.update_dfield().update_dtfsf()
    metal.update(plane)
    plane.update_efield(metal)

    plane.update_epbc()
    plane.update_bfield().update_btfsf()
    plane.update_hfield()
    
    # imshow(plane.ezfield, "/tmp/%.3d.png", t)
    hdf5.require_group("timeline/"+str(t))
    hdf5["timeline"][str(t)]["ez"] = plane.ezfield


hdf5.attrs["freq"] = freq
hdf5.attrs["deltat"] = deltat
hdf5.close()
