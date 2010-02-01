#!/usr/bin/env python
#-*- mode: python -*-

import convention

from fdtd import source, grid, mesher

from fdtd.algorithm.twodim.freespace import update_efield, update_hfield

# program start

new_efield = grid.Plane(shape=(301,301), timestep=1, spacestep=2*3*10**8)
new_efield.eps[180:,0:] *= 2
new_hfield = grid.Plane(shape=(301,301), timestep=1, spacestep=2*3*10**8)
new_hfield.eps[180:,0:] *= 2


for step in range(1,600):
    new_efield.y[150,150] += float(mpmath.sin(step*mpmath.pi/6.125))*2
    new_efield = update_efield( new_efield, new_hfield )
    new_hfield.z[150,150] += float(mpmath.sin(step*mpmath.pi/6.125))*2
    new_hfield = update_hfield( new_efield, new_hfield )
    

    h = numpy.array(new_hfield.z, dtype="float")
    for i in xrange(1,300):
        for j in xrange(1,300):
            if (i+j)%2 == 1:
                h[i,j] = ( h[i+1,j] + h[i-1,j] + h[i,j+1] + h[i,j-1] ) / 4
    pylab.imshow( h, interpolation="quadric", norm=matplotlib.colors.Normalize(-0.3,0.3,True) )
    pylab.colorbar()
    pylab.grid(True)
    pylab.savefig("result/fdtd_plane-%.3d.png" % step)
    pylab.clf()

    d = numpy.array(new_hfield.z[0:,150], dtype="float")

    for i in xrange(1,len(d)-1):
        if i%2==0:
            d[i] = ( d[i-1] + d[i+1] ) / 2

    pylab.plot( d )
    pylab.ylim((-0.3,0.3))
    pylab.grid(True)
    pylab.savefig("result_slice/fdtd_plane_slice-%s.png" % str(step))
    pylab.clf()

if "Darwin" in os.uname():
    os.system("open result")
    os.system("open result_slice")

