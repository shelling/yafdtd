#!/usr/bin/env python
#-*- mode: python -*-
import convention
import os, csv, re

from fdtd import source
from fdtd.algorithm.twodim import freespace, bpml
from fdtd.grid import Plane
from fdtd.utils import *

plane = Plane( (31,31), "TM")
bpml.append_pml( plane )

for t in range(0,120):
    bpml.update_efield( plane )
    plane.ezfield[plane.shape[0]/2, plane.shape[1]/2] = source.sin_oft(t, 10)
    bpml.update_hfield( plane )
    save_field(plane.ezfield, "result/twod-testing-%.3d.png", t, [-1,1])
    print t