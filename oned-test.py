#!/usr/bin/env python
#-*- mode: python -*-

import sys, os, csv, re, shutil, h5py
sys.path.append("./lib")

from fdtd import source
from fdtd.algorithm.onedim import *
from fdtd.grid import String
from fdtd.utils import *

string = String(31)
string.source = source.HardSource(source.sin_oft, (5,), string.shape[0]/2)

prepare("result")

name = "oned-test"

hdf5 = h5py.File("result/%s.hdf5" % name,"w")
hdf5.attrs["name"] = name
hdf5.require_group("timeline")

for t in range(0,200):
    string.update_efield()\
          .update_abc()\
          .update_source(t)\
          .update_hfield()\
          # .plot("result/oned-testing-%.3d.png", t)
    hdf5.require_group("timeline/"+str(t))
    hdf5["timeline"][str(t)]["ex"] = string.efield
    hdf5["timeline"][str(t)]["hy"] = string.hfield
    print t

hdf5.close()

open("result")
