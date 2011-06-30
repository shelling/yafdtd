#!/usr/bin/env python
from mpi4py import MPI
import os, sys, numpy, pylab

sys.path.append(".")

from yafdtd.grid import Plane, PBCPlane, UPMLPlane, XTFSFPlane, DispersivePlane, PolarDPlane, PlaneDecorator
from yafdtd.utils import *
from scipy.constants import c
from math import sin, pi
from yafdtd.geometry import circle

class MPIXEdgePlane(PlaneDecorator):
    def __init__(self, orig):
        super(MPIXEdgePlane, self).__init__(orig)
        return None

    def send_hpbc(self):
        self.mpi_comm.send(self.hyfield[self.shape[0]-1], dest=self.mpi_next, tag=0)
        return self

    def recv_hpbc(self):
        return self

    def send_epbc(self):
        self.mpi_comm.send(self.ezfield[0], dest=self.mpi_prev, tag=1)
        return self

    def recv_hpbc(self):
        return self


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


plane = MPIXEdgePlane(UPMLPlane(PBCPlane(Plane("mpi2d", (30, 90)))))
plane.pbc(x = False, y = True)
plane.mpi_comm = comm
plane.mpi_size = size
plane.mpi_rank = rank
plane.mpi_prev = rank-1
plane.mpi_next = rank+1

if rank == size-1:
    plane.mpi_next = 0
if rank == 0:
    plane.mpi_prev = size-1

if rank == 0:
    finalplane = Plane("final", (90,90))


for t in range(100):
    plane.send_hpbc()
    plane.update_hpbc(hyedgex=plane.mpi_comm.recv(source=plane.mpi_prev, tag=0))
    plane.update_dfield()
    plane.update_efield()

    if rank == 0:
        print t
        plane.ezfield[5,5] = sin(2*pi*freq*t*deltat)

    plane.send_epbc()
    plane.update_epbc(ezedgex=plane.mpi_comm.recv(source=plane.mpi_next, tag=1))
    plane.update_bfield()
    plane.update_hfield()


    ez = comm.gather(plane.ezfield, root=0)
    if rank == 0:
        finalplane.ezfield = numpy.concatenate(ez)
        finalplane.imshow_ez("/tmp/%.3d.png"%t)
