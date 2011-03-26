#!/usr/bin/env python
#-*- mode: python -*-

import sys, os, math, h5py, numpy

from yafdtd.source import sin_oft
from yafdtd.grid import Cube
from yafdtd.utils import *
from scipy.constants import c, epsilon_0, mu_0


name = "threed-test"
outdir = "result/%s" % name
prepare(outdir)

hdf5 = h5py.File("%s/%s.hdf5" % (outdir, name), "w")
hdf5.attrs["name"] = name
hdf5.require_group("timeline")

length = 31

cube = Cube((length,length,length))

for t in range(100):
    cube.update_dfield()
    cube.update_efield()
    cube.ezfield[15,15,:] = sin_oft(0.005*t)
    cube.update_bfield()
    cube.update_hfield()
    
    hdf5.require_group("timeline/"+str(t))
    hdf5["timeline"][str(t)]["ez"] = cube.ezfield[:,:,15]
    print t

hdf5.close()
