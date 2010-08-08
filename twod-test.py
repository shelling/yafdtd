#!/usr/bin/env python
#-*- mode: python -*-
import convention
import os, csv, re

from fdtd import source
from fdtd.algorithm.twodim import freespace, bpml
from fdtd.grid import Plane
from fdtd.utils import *

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FixedLocator, FormatStrFormatter

def save_field_surf(field, filename_pattern, id):
    x = numpy.arange(0,field.shape[0])
    y = numpy.arange(0,field.shape[1])
    x, y = numpy.meshgrid(x, y)
    fig = pylab.figure()
    ax = fig.gca(projection="3d")
    ax.plot_surface(x, y, field, rstride=1, cstride=1, cmap=cm.jet, linewidth=0, antialiased=False, norm=matplotlib.colors.Normalize(-1,1,True))
    fig.gca().set_zlim3d([-1,1])
    pylab.savefig(filename_pattern % id)
    return None


plane = Plane( (31,31), "TM")
bpml.append_pml( plane )
bpml.plot_pml_params(plane, "/tmp/a.png")


for t in range(0,500):
    bpml.update_efield( plane )
    plane.ezfield[plane.shape[0]/2, plane.shape[1]/2] = source.sin_oft(t, 10)
    bpml.update_hfield( plane )
    save_field_surf(plane.ezfield, "result/twod-testing-surface-%.3d.png", t )
    save_field(plane.ezfield, "result/twod-testing-%.3d.png", t, [-1,1])
    print t
