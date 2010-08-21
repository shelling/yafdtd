#!/usr/bin/env python
#-*- mode: python -*-
import convention
import os, csv, re

from fdtd import source
from fdtd.algorithm.onedim import *
from fdtd.grid import String
from fdtd.utils import *

string = String(31)

for t in range(1,70):
    string.update_efield()
    update_abc(string)
    update_source(string, string.shape[0]/2, source.sin_oft, (t,5))
    string.update_hfield()
    string.plot("result/oned-testing-%.3d.png", t)
    print t

if "Darwin" in os.uname():
    os.system("open result")
