#!/usr/bin/env python
#-*- mode: python -*-

import convention
import math
import os, csv, re

from fdtd import source
from fdtd.algorithm.onedim import *

from fdtd.grid import String

def save_field(field, filename_pattern, id, axis=None):
    """
    shortcut for saving file through matplotlib
    
    Arguments:
    - `field`:
    - `filename_pattern`:
    - `id`:
    - `axis`:
    """
    pylab.grid(True)
    pylab.plot(field)
    pylab.ylim([-1,1])
    pylab.savefig(filename_pattern % id)
    pylab.clf()
    return None

string = String(31)

efield_lm1 = 0
efield_lm2 = 0
efield_rm1 = 0
efield_rm2 = 0

for t in range(1,70):

    update_efield(string)

    string.efield[0]  = efield_lm2
    efield_lm2 = efield_lm1
    efield_lm1 = string.efield[1]

    string.efield[string.efield.shape[0]-1] = efield_rm2
    efield_rm2 = efield_rm1
    efield_rm1 = string.efield[string.efield.shape[0]-2]

    xcenter = string.efield.shape[0]/2
    string.efield[xcenter] = source.gaussian_oft(t, 30, 5)
    
    update_hfield(string)

    save_field(string.efield, "result/oned-testing-%.3d.png", t)
    print t



if "Darwin" in os.uname():
    os.system("open result")
