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
auxiliary.source = source.HardSource(source.sin_oft, (10,), 3)


for t in range(0,50):
    auxiliary.update_efield().update_abc()
    auxiliary.update_source(t)
    for i in range(10,21):
        plane.ezfield[i,10] = plane.ezfield[i,10] + 0.5 * auxiliary.hfield[10-1]
        plane.ezfield[i,21] = plane.ezfield[i,21] - 0.5 * auxiliary.hfield[21]
    plane.update_efield()
    
    auxiliary.update_hfield()
    # plane.ezfield[plane.shape[0]/2, plane.shape[1]/2] = source.sin_oft(t, 10)
    plane.update_hfield()

    for i in range(10,21):
        plane.hxfield[i,10-1] = plane.hxfield[i,10-1] + 0.5 * auxiliary.efield[10]
        plane.hxfield[i,21]   = plane.hxfield[i,21]   - 0.5 * auxiliary.efield[21]
    for j in range(10,21):
        plane.hyfield[10-1,j] = plane.hyfield[10-1,j] - 0.5 * auxiliary.efield[j]
        plane.hyfield[21,j]   = plane.hyfield[21,j]   + 0.5 * auxiliary.efield[j]
    plane.plot("result/twod-testing-surface-%.3d.png", t)
    auxiliary.plot("result/auxiliary-%.3d.png", t)
    print t

if "Darwin" in os.uname():
    os.system("open result")
