#!/usr/bin/env python
#-*- mode: python -*-

import sys, os, math, h5py, numpy

from yafdtd.source import HardSource, TFSF, sin_oft
from yafdtd.grid import Plane
from yafdtd.utils import *
from scipy.constants import c, epsilon_0, mu_0


name = "twod-test"
outdir = "result/%s" % name
prepare(outdir)

hdf5 = h5py.File("%s/%s.hdf5" % (outdir, name), "w")
hdf5.attrs["name"] = name 
hdf5.require_group("timeline")

length = 31
edge = 8
dx = 0.01
dt = dx/c
sigma = 5000

plane = Plane((length,length))
# plane.append( upml.UPML(plane.shape, 8) )
# plane.append( TFSF(length, function=sin_oft, thick=edge) )
# plane.append( HardSource(sin_oft, (10,), (15,15) ) )


for t in range(0,100):
    plane.update_dfield()
    plane.update_efield()
    plane.ezfield[16,16] = sin_oft(0.005*t)
    plane.update_bfield()
    plane.update_hfield()

    hdf5.require_group("timeline/"+str(t))
    hdf5["timeline"][str(t)]["ez"] = plane.ezfield
    print t

hdf5.close()

open(outdir)
