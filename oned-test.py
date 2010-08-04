#!/usr/bin/env python
#-*- mode: python -*-

import matplotlib
matplotlib.use("Agg")                   # for linux without desktop env

import pylab
import numpy
import math
import os, csv, re

efield = numpy.zeros(11)
hfield = numpy.zeros(11)


def update_efield(efield, hfield):
    """
    update efield
    
    Arguments:
    - `efield`:
    """
    for x in range(1, efield.shape[0]-1):
        efield[x] = efield[x] + 0.5 * ( hfield[x-1] - hfield[x] )


def update_hfield(efield, hfield):
    """
    update hfield
    
    Arguments:
    - `efield`:
    - `hfield`:
    """
    for x in range(0, hfield.shape[0]-1):
        hfield[x] = hfield[x] + 0.5 * ( efield[x] - efield[x+1] )


def gaussian(center, width):
    """
    Gaussian Pulse generater
    
    Arguments:
    - `center`:
    - `width`:
    """
    return math.exp( -0.5 * math.pow((center - t)/width, 2.0) )

def sin_oft(t,f):
    """
    sine of t
    
    Arguments:
    - `t`:
    """
    return math.sin(t*f*math.pi/180)


efield_lm1 = 0
efield_lm2 = 0
efield_rm1 = 0
efield_rm2 = 0

for t in range(1,140):

    update_efield(efield, hfield)

    efield[0]  = efield_lm2
    efield_lm2 = efield_lm1
    efield_lm1 = efield[1]

    efield[efield.shape[0]-1] = efield_rm2
    efield_rm2 = efield_rm1
    efield_rm1 = efield[efield.shape[0]-2]

    
    xcenter = efield.shape[0]/2
    efield[xcenter] = sin_oft(t,10)

    
    update_hfield(efield, hfield)

    pylab.grid(True)
    pylab.plot( efield )
    pylab.ylim([-1,1])
    pylab.savefig("result/oned-testing-%.3d.png" % t)
    pylab.clf()
    print t



if "Darwin" in os.uname():
    os.system("open result")
