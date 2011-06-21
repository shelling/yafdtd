#!/usr/bin/env python
from mpi4py import MPI
import os, sys, numpy, pylab

sys.path.append(".")

from yafdtd.grid import Plane, PBCPlane, UPMLPlane, XTFSFPlane, DispersivePlane, PolarDPlane
from yafdtd.utils import *
from scipy.constants import c
from math import sin, pi
from yafdtd.geometry import circle


comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

n = numpy.zeros(3)
n.fill(rank)
r = comm.gather(n, root=0)
if rank == 0:
    print numpy.concatenate(r)

##################### main FDTD ####################

deltax = 10**-9
deltat = deltax/(2*c)
freq   = 4*10**15


plane = UPMLPlane(PBCPlane(Plane("mpi2d", (300, 900))))
plane.pbc(x = False, y = True)

if rank == 0:
    finalplane = Plane("final", (900,900))


for t in range(300):

    if rank < size-1:
        comm.send(plane.hyfield[299], dest=rank+1, tag=0)
    if rank > 0:
        hedge = comm.recv(source=rank-1, tag=0)
    if rank == size-1:
        comm.send(plane.hyfield[299], dest=0, tag=0)
    if rank == 0:
        hedge = comm.recv(source=size-1, tag=0)

    plane.update_hpbc(hyedgex=hedge)
    plane.update_dfield()
    plane.update_efield()

    if rank == 0:
        print t
        plane.ezfield[15,15] = sin(2*pi*freq*t*deltat)

    if rank > 0:
        comm.send(plane.ezfield[0], dest=rank-1, tag=1)
    if rank < size-1:
        eedge = comm.recv(source=rank+1, tag=1)
    if rank == 0:
        comm.send(plane.ezfield[0], dest=size-1, tag=1)
    if rank == size-1:
        eedge = comm.recv(source=0, tag=1)
 
    plane.update_epbc(ezedgex=eedge)
    plane.update_bfield()
    plane.update_hfield()


    ez = comm.gather(plane.ezfield, root=0)
    if rank == 0:
        finalplane.ezfield = numpy.concatenate(ez)
        # finalplane.imshow_ez("/tmp/%.3d.png"%t)
