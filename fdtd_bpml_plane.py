#!/usr/bin/env python
#-*- mode: python -*-

import convention

from fdtd import source, grid, mesher

from fdtd.algorithm.twodim.bpml import update_efield, update_hfield
# program start

new_efield = grid.Plane(shape=(301,301), timestep=1, spacestep=2*3*10**8)
new_efield.eps[:180,0:] *= 2
new_efield.sigmae = grid.PlaneBase(new_efield.shape)
new_efield.sigmah = grid.PlaneBase(new_efield.shape)

new_hfield = grid.Plane(shape=(301,301), timestep=1, spacestep=2*3*10**8)
new_hfield.eps[:180,0:] *= 2
new_hfield.zx = numpy.zeros(new_hfield.shape)
new_hfield.zy = numpy.zeros(new_hfield.shape)
new_hfield.sigmae = grid.PlaneBase(new_hfield.shape)
new_hfield.sigmah = grid.PlaneBase(new_hfield.shape)


for step in range(1,250):
    new_efield.y[149:152,149:152] += float(mpmath.sin(step*mpmath.pi/6.125))
    new_efield = update_efield( new_efield, new_hfield )
    new_hfield.zx[150,150] += float(mpmath.sin(step*mpmath.pi/6.125))/2
    new_hfield.zy[150,150] += float(mpmath.sin(step*mpmath.pi/6.126))/2
    new_hfield = update_hfield( new_efield, new_hfield )

    h = numpy.array(new_hfield.z, dtype="float")
    
    for i in xrange(1,300):
        for j in xrange(1,300):
            if (i+j)%2 == 1:
                h[i,j] = ( h[i+1,j] + h[i-1,j] + h[i,j+1] + h[i,j-1] ) / 4
                
    pylab.imshow( h, interpolation="quadric", norm=matplotlib.colors.Normalize(-1,1.8,True) )
    pylab.colorbar()

    pylab.savefig("result/fdtd_plane-%.3d.png" % step)
    pylab.clf()
    print step


if "Darwin" in os.uname():
    os.system("open result")


