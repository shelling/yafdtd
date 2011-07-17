#!/usr/bin/env python
#-*- mode: python -*-

import sys, os, csv, re, shutil, h5py, pylab
sys.path.append(".")

from yafdtd.source import *
from yafdtd.grid import String
from yafdtd.utils import *
from scipy.constants import c, epsilon_0
from math import pi, sin, cos
from sys import stdout

string1 = String(201)
string1.enter = 5

string2 = String(201)
string2.enter = 5

for t in range(1200):
    stdout.write("\b"*80+str(t))

    # string1.update(sin(2*pi*0.025*t))

    # string1.update(gaussian(t, 200, 60))
    string2.update(cos(2*pi*0.025*t)*gaussian(t, 200, 60))
    
    # pylab.plot(string1.efield)
    pylab.plot(string2.efield)
    pylab.ylim(-1,1)
    pylab.savefig("/tmp/gaussian-%.3d.png"%t)
    pylab.clf()
