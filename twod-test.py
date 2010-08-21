#!/usr/bin/env python
#-*- mode: python -*-
import convention
import os, csv, re, gc

from fdtd import source
from fdtd.algorithm.twodim import freespace, upml
from fdtd.grid import Plane, String
from fdtd.utils import *

plane = Plane( (31,31), "TM")
upml.append_pml( plane )

auxiliary = String(31)


for t in range(0,50):
    plane.update_efield()
    plane.ezfield[plane.shape[0]/2, plane.shape[1]/2] = source.sin_oft(t, 10)
    plane.update_hfield()
    plane.plot3d("result/twod-testing-surface-%.3d.png", t)
    print t

if "Darwin" in os.uname():
    os.system("open result")
