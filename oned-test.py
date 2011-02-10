#!/usr/bin/env python
#-*- mode: python -*-

import sys, os, csv, re, shutil, h5py

from yafdtd import source
from yafdtd.algorithm.onedim import *
from yafdtd.grid import String
from yafdtd.utils import *
from scipy.constants import c, epsilon_0

dt = 10**-9
dx = dt*c*2
f  = dt * (10**16)

name = "oned-test"
outdir = "result/%s" % name
prepare(outdir)

string = String(31)
string.source = source.HardSource(source.sin_oft, (f,), string.shape[0]/2)

hdf5 = h5py.File("%s/%s.hdf5" % (outdir, name),"w")
hdf5.attrs["name"]  = name
hdf5.attrs["dt"]    = dt
hdf5.attrs["dx"]    = dx
hdf5.require_group("timeline")

for t in range(0,500):
    string.update_dfield()\
          .update_efield()\
          .update_abc()\
          .update_source(t*dt)\
          .update_bfield()\
          .update_hfield()
    hdf5.require_group("timeline/"+str(t))
    hdf5["timeline"][str(t)]["ex"] = string.efield
    hdf5["timeline"][str(t)]["hy"] = string.hfield
    print(t)

hdf5.close()

open(outdir)
