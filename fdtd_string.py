#!/usr/bin/env python

import os
import sys
sys.path += ["./lib"]
import fdtd

import matplotlib
matplotlib.use("Agg")

import math
import numpy
# import scipy

import mpmath
import sympy

class Grid1D(object):
    """On Dimension Grid Object
    """
    
    def __init__(self, step = { "time":2, "space":2 }):
        """
        
        Arguments:
        - `step`:
        - `"space":2 }`:
        """
        self._step = step



class FDTD(object):

    @classmethod
    def next_efield(self, previous_efield, previous_hfield, step = {"time":2, "space":2}):

        current_efield = numpy.zeros_like(previous_hfield)
#         print step["time_step"]

        for location in current_efield:
            current_efield[location] = previous_efield[location] + (previous_hfield[location+1] - previous_hfield[location-1]) * step["space"] / step["time"]
        # main algorithm
        # half-completed
        return current_efield


    @classmethod
    def next_hfield(self, previous_efield, step = {"time":2, "space":2}):
        current_hfield
        return current_hfield


previous_fieid_array = numpy.zeros(100)
two_previous_fieldarray = numpy.zeros(100)

print previous_fieid_array
print FDTD.next_efield(two_previous_fieldarray, two_previous_fieldarray)
