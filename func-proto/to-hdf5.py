#!/usr/bin/env python

import h5py
import numpy

file = h5py.File("result.hdf5","w")

data = numpy.arange(0,10000)
data.shape = (100,100)

file["data"] = data

