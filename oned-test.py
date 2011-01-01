#!/usr/bin/env python
#-*- mode: python -*-
import convention
import os, csv, re, shutil, h5py

from fdtd import source
from fdtd.algorithm.onedim import *
from fdtd.grid import String
from fdtd.utils import *

string = String(31)
string.source = source.HardSource(source.sin_oft, (5,), string.shape[0]/2)

if os.path.isdir("result"):
  shutil.rmtree("result")
os.mkdir("result")

hdf5 = h5py.File("result/result.hdf5","w")
hdf5.require_group("timeline")

for t in range(0,70):
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
