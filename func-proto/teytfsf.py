#!/usr/bin/env python
#-*- mode: python -*-

import sys, os, math, h5py, numpy
sys.path.append(".")

from yafdtd.grid import Plane, PBCPlane, UPMLPlane, YTFSFPlane, DispersivePlane
from yafdtd.grid import String
from yafdtd.utils import *
from scipy.constants import c, epsilon_0, mu_0
from math import sin, pi

name = "teytfsf"
outdir = "result/%s" % name
prepare(outdir)
hdf5 = h5py.File("%s/%s.hdf5" % (outdir, name), "w")
hdf5.attrs["name"] = name 
hdf5.require_group("timeline")

length = 61
deltax = 10**-9
deltat = deltax/(2*c)
freq   = 4*10**15

plane = DispersivePlane(YTFSFPlane(UPMLPlane(PBCPlane(Plane((length,length))))))
plane.pbcy = False
plane.pmlx = False
plane.pml_thick = 5
plane.set_pml()

teinc = String(length)
teinc.enter = 2

for t in range(0,600):
    teinc.update(sin(2*pi*freq*t*deltat))

    plane.update_hpbc()
    plane.update_dfield()
    plane.dxfield[:,10] -= 0.5 * teinc.hfield[9]
    plane.dxfield[:,51] += 0.5 * teinc.hfield[51]
    plane.update_efield()

    plane.update_epbc()
    plane.update_bfield()
    plane.bzfield[:,9]  += 0.5 * teinc.efield[10]
    plane.bzfield[:,51] -= 0.5 * teinc.efield[51]
    plane.update_hfield()
    
    hdf5.require_group("timeline/"+str(t))
    hdf5["timeline"][str(t)]["ez"] = plane.hzfield
    plot(plane.hzfield[31], "/tmp/ez%.3d.png", t)
    print t

hdf5.close()
