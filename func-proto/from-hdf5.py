#!/usr/bin/env python

import h5py
import numpy

file = h5py.File("result.hdf5","r")
data = file["data"]
print numpy.array(data)
