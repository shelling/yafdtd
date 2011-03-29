#!/usr/bin/env python
#-*- mode: python -*-

import sys, os, math, h5py, numpy

from yafdtd.source import HardSource, TFSF, sin_oft
from yafdtd.grid import Plane, PBCPlane
from yafdtd.utils import *
from scipy.constants import c, epsilon_0, mu_0


name = "twod-test"
outdir = "result/%s" % name
prepare(outdir)

hdf5 = h5py.File("%s/%s.hdf5" % (outdir, name), "w")
hdf5.attrs["name"] = name 
hdf5.require_group("timeline")

length = 61
edge = 8
dx = 0.01
dt = dx/c
sigma = 5000

plane = Plane((length,length))
plane = PBCPlane(plane)
plane.pbcx = False


for t in range(0,100):
    plane.update_hpbc()
    plane.update_dfield()
    plane.update_efield()

    plane.ezfield[0,0] = sin_oft(0.005*t)

    plane.update_epbc()
    plane.update_bfield()
    plane.update_hfield()
    
    plane.hzfield[0,0] = sin_oft(0.005*t)

    hdf5.require_group("timeline/"+str(t))
    hdf5["timeline"][str(t)]["ez"] = plane.ezfield
    print t

hdf5.close()
