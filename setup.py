#!/usr/bin/env python

from distutils.core import setup

setup(
  name            = "yafdtd",
  version         = "1.0,0",
  description     = "Yet Another Finite-Difference Time-Domain Framework",
  author          = "shelling",
  author_email    = "navyblueshellingford@gmail.com",
  url             = None,
  packages        = [
          'yafdtd',
          'yafdtd.algorithm',
          'yafdtd.algorithm.threedim',
          'yafdtd.algorithm.twodim',
          'yafdtd.geometry',
  ],
)
