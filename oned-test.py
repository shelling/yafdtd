#!/usr/bin/env python
#-*- mode: python -*-
import convention
import os, csv, re

from fdtd import source
from fdtd.algorithm.onedim import *
from fdtd.grid import String
from fdtd.utils import *

string = String(31)
string.source = source.HardSource(source.sin_oft, (5,), string.shape[0]/2)

for t in range(1,70):
    string.update_efield()\
          .update_abc()\
          .update_source((t))\
          .update_hfield()\
          .plot("result/oned-testing-%.3d.png", t)
    print t

if "Darwin" in os.uname():
    os.system("open result")
