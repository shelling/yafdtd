#!/usr/bin/env python
#-*- mode: python -*-
import convention
import os, csv, re, gc, math

from fdtd.source import HardSource, TFSF, sin_oft
from fdtd.algorithm.twodim import freespace, upml
from fdtd.grid import Plane, String
from fdtd.utils import *
from scipy.constants import c, epsilon_0

if os.path.isdir("result"):
  shutil.rmtree("result")
os.mkdir("result")

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
    plane.plot3d("result/twod-testing-%.3d.png", t, range=[-3,3])
    print t

open("result")
