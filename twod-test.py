#!/usr/bin/env python
#-*- mode: python -*-
import convention
import os, csv, re, gc

from fdtd import source
from fdtd.algorithm.twodim import freespace, upml
from fdtd.grid import Plane, String
from fdtd.utils import *

length = 31
edge = 8

plane = Plane( (length,length), "TM")
plane.append( upml.UPML(plane.shape, 8) )
plane.source = source.TFSF(length, source.sin_oft, edge)

for t in range(0,100):
    plane.update_source(t)\
         .update_efield()\
         .update_hfield()\
         .plot("result/twod-testing-%.3d.png", t)

    print t

if "Darwin" in os.uname():
    os.system("open result")
