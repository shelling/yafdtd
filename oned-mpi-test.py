#!/usr/bin/env python
import convention
import os, csv, re, commands

from mpi4py import MPI

from fdtd import source
from fdtd.algorithm.onedim import *
from fdtd.grid import String
from fdtd.utils import *

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

# host = commands.getoutput("hostname")
# print "I am process " + str(rank) + " of " + str(size) + " on " + host

cells = 30
string = String(30/size)

left = 0.0
right = 0.0

for t in range(0,1000):
    update_efield(string)
    
    comm.Barrier()
    
    if rank == 1:
        string.efield[0] = string.efield[0] + 0.5 * ( left - string.hfield[0] )
    
    comm.Barrier()

    if rank == 0:
        update_abc_left(string)
        comm.send(string.efield[-1], dest=1, tag=0)
        right = comm.recv(source=1, tag=1)
    elif rank == size-1:
        update_abc_right(string)
        comm.send(string.efield[0], dest=rank-1, tag=1)
        left = comm.recv(source=0, tag=0)
    else:
        pass
    
    comm.Barrier()
    
    if rank == 0:
        update_source(string, string.shape[0]/2, source.sin_oft, (t,5))

    update_hfield(string)
    
    comm.Barrier()
    
    if rank == 0:
        string.hfield[-1] = string.hfield[-1] + 0.5 * ( string.efield[-1] - right )
    
    comm.Barrier()

    if rank == 0:
        comm.send(string.hfield[-1], dest=1, tag=0)
        right = comm.recv(source=1, tag=1)
    elif rank == size-1:
        comm.send(string.hfield[0], dest=0, tag=1)
        left = comm.recv(source=0, tag=0)
    else:
        pass
    
    comm.Barrier()
    
    efield = comm.gather(string.efield)
    if rank == 0:
        efield = numpy.array(efield).flatten()
        save_field(efield, "result/oned-mpi-testing-%.3d.png", t)
        print t
