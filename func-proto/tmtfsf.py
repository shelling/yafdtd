#!/usr/bin/env python
#-*- mode: python -*-

import sys, os, math, h5py, numpy
sys.path.append(".")

from yafdtd.grid import Plane, PBCPlane, UPMLPlane, YTFSFPlane
from yafdtd.grid import String
from yafdtd.utils import *
from scipy.constants import c, epsilon_0, mu_0
from math import sin, pi


name = "tmtfsf"
outdir = "result/%s" % name
prepare(outdir)
hdf5 = h5py.File("%s/%s.hdf5" % (outdir, name), "w")
hdf5.attrs["name"] = name 
hdf5.require_group("timeline")

length = 61
deltax = 10**-9
deltat = deltax/(2*c)
freq   = 4*10**15

plane = YTFSFPlane(UPMLPlane(PBCPlane(Plane((length,length)))))
plane.pbcy = False
plane.pmlx = False
plane.pml_thick = 5
plane.set_pml()
plane.tminc.enter = 2
plane.xtfsf = [None, None]


for t in range(0,600):
    plane.tminc.update(sin(2*pi*freq*t*deltat))

    plane.update_hpbc()
    plane.update_dfield().update_dtfsf()
    plane.update_efield()

    plane.update_epbc()
    plane.update_bfield().update_btfsf()
    plane.update_hfield()
    
    hdf5.require_group("timeline/"+str(t))
    hdf5["timeline"][str(t)]["ez"] = plane.ezfield
    plot(plane.ezfield[10,:], "/tmp/tmtfsf-%.3d.png", t)
    print t

hdf5.close()
