#!/usr/bin/env python
#-*- mode: python -*-

import os, math


from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FixedLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy

X = numpy.arange(-10, 10, 0.25)
Y = numpy.arange(-10, 10, 0.25)
X, Y = numpy.meshgrid(X, Y)
r= (X**2+Y**2)
Z = numpy.cos(r*math.pi/72.0)*numpy.exp(-r/100)

plt.gca(projection='3d').plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.jet, linewidth=0, antialiased=False)


plt.savefig("/tmp/a.png")
os.system("open /tmp/a.png")

# fig = plt.figure()
# x = numpy.arange(-10,10,0.25)
# y = numpy.arange(-10,10,0.25)
# x, y = numpy.meshgrid(x, y)

# ax = fig.gca(projection="3d")
# surf = ax.plot_surface(x, y, x+y)


# fig.colorbar(surf, shrink=0.5, aspect=5)
# plt.savefig("/tmp/b.png")
# os.system("open /tmp/b.png")

        
