#!/usr/bin/env python
#-*- mode: python -*-

from sympy import *

x = Symbol("x")
p = Poly((1+x**2)**4, x)
q = p.diff()
print p(1)
print q(1)

