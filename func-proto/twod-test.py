#!/usr/bin/env python
#-*- mode: python -*-

import sys, os, math, h5py, numpy
sys.path.append(".")

from yafdtd.grid import Plane, PBCPlane, UPMLPlane
from yafdtd.utils import *
from scipy.constants import c, epsilon_0, mu_0
from math import sin, pi

name = "twod-test"
outdir = "result/%s" % name
prepare(outdir)
hdf5 = h5py.File("%s/%s.hdf5" % (outdir, name), "w")
hdf5.attrs["name"] = name 
hdf5.require_group("timeline")

length = 301
deltax = 10**-9
deltat = deltax/(2*c)
freq   = 4*10**15

plane = UPMLPlane(PBCPlane(Plane((length,length))))

plane.pbcx = False
plane.pbcy = False
# plane.pmly = False
plane.pml_thick = 20
plane.set_pml()


for t in range(0,600):
    plane.update_hpbc()
    plane.update_dfield()
    plane.update_efield()

    plane.ezfield[151,151] = sin(2*pi*freq*t*deltat)

    plane.update_epbc()
    plane.update_bfield()
    plane.update_hfield()
    
    plane.hzfield[151,151] = sin(2*pi*freq*t*deltat)

    hdf5.require_group("timeline/"+str(t))
    hdf5["timeline"][str(t)]["ez"] = plane.ezfield
    print t

hdf5.close()
