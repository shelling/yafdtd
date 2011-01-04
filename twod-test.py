#!/usr/bin/env python
#-*- mode: python -*-

import sys, os, math, h5py, numpy
sys.path.append("lib")

from fdtd.source import HardSource, TFSF, sin_oft
from fdtd.algorithm.twodim import freespace, upml
from fdtd.grid import Plane, String
from fdtd.utils import *
from scipy.constants import c, epsilon_0

if os.path.isdir("result"):
  shutil.rmtree("result")
os.mkdir("result")

hdf5 = h5py.File("result/result.hdf5", "w")
hdf5.require_group("timeline")

length = 61
edge = 8
dx = 0.01
dt = dx/c
sigma = 5000

plane = Plane( (length,length), "TM")
plane.append( upml.UPML(plane.shape, 8) )
plane.append( TFSF(length, function=sin_oft, thick=edge) )
# plane.append( HardSource(sin_oft, (10,), (15,15) ) )

for i in range(edge, length-edge):
    for j in range(edge, length-edge):
        dist = math.hypot(i-length/2,j-15)
        if dist < 5:
            plane.ga[i,j] = 1.0/(30 + (sigma * dt / epsilon_0))
            plane.gb[i,j] = sigma * dt / epsilon_0

for t in range(0,300):
    plane.update_efield()
    plane.update_source(t)
    plane.update_hfield()
    # surf(plane.ezfield, "result/twod-testing-%.3d.png", t, intensity=[-3,3])
    hdf5.require_group("timeline/"+str(t))
    hdf5["timeline"][str(t)]["ez"] = plane.ezfield
    print t

hdf5.close()

open("result")
