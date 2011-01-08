#!/usr/bin/env python
#-*- mode: python -*-

import convention

from fdtd import source, grid, mesher

from fdtd.algorithm.twodim.bpml import update_efield, update_hfield
# program start

new_efield = grid.Plane(shape=(301,301), timestep=1, spacestep=2*3*10**8)
#new_efield.eps[:180,0:] *= 2
new_efield.sigmae = grid.PlaneBase(new_efield.shape)
new_efield.sigmah = grid.PlaneBase(new_efield.shape)

###
# new_efield.sigmah.x[0,0:301] = new_efield.sigmah.x[300,0:301] = 37000
# new_efield.sigmah.x[1,1:300] = new_efield.sigmah.x[299,1:300] = 25000
# new_efield.sigmah.x[2,2:299] = new_efield.sigmah.x[298,2:299] = 19000
# new_efield.sigmah.x[3,3:298] = new_efield.sigmah.x[297,3:298] = 15000
# new_efield.sigmah.x[4,4:297] = new_efield.sigmah.x[296,4:297] = 12000
# new_efield.sigmah.x[5,5:296] = new_efield.sigmah.x[295,5:296] = 80000
# new_efield.sigmah.x[6,6:295] = new_efield.sigmah.x[294,6:295] = 80000
# new_efield.sigmah.x[7,7:294] = new_efield.sigmah.x[293,7:294] = 80000
# new_efield.sigmah.x[8,8:293] = new_efield.sigmah.x[292,8:293] = 80000
# new_efield.sigmah.x[9,9:292] = new_efield.sigmah.x[291,9:292] = 80000

new_efield.sigmae.x[0,0:301] = new_efield.sigmae.x[300,0:301] = 37000
new_efield.sigmae.x[1,1:300] = new_efield.sigmae.x[299,1:300] = 25000
new_efield.sigmae.x[2,2:299] = new_efield.sigmae.x[298,2:299] = 19000
new_efield.sigmae.x[3,3:298] = new_efield.sigmae.x[297,3:298] = 15000
new_efield.sigmae.x[4,4:297] = new_efield.sigmae.x[296,4:297] = 12000
new_efield.sigmae.x[5,5:296] = new_efield.sigmae.x[295,5:296] = 80000
new_efield.sigmae.x[6,6:295] = new_efield.sigmae.x[294,6:295] = 80000
new_efield.sigmae.x[7,7:294] = new_efield.sigmae.x[293,7:294] = 80000
new_efield.sigmae.x[8,8:293] = new_efield.sigmae.x[292,8:293] = 80000
new_efield.sigmae.x[9,9:292] = new_efield.sigmae.x[291,9:292] = 80000

###
new_efield.sigmae.x[0:301,0] = new_efield.sigmae.x[0:301,300] = 37000
new_efield.sigmae.x[1:300,1] = new_efield.sigmae.x[1:300,299] = 25000
new_efield.sigmae.x[2:299,2] = new_efield.sigmae.x[2:299,298] = 19000
new_efield.sigmae.x[3:298,3] = new_efield.sigmae.x[3:298,297] = 15000
new_efield.sigmae.x[4:297,4] = new_efield.sigmae.x[4:297,296] = 12000


###
pylab.imshow(numpy.array(new_efield.sigmae.x + new_efield.sigmae.y, dtype="float"))
pylab.savefig("field-sigma-sum.png")
pylab.clf()
###

new_hfield = grid.Plane(shape=(301,301), timestep=1, spacestep=2*3*10**8)
# new_hfield.eps[:180,0:] *= 2
new_hfield.zx = numpy.zeros(new_hfield.shape)
new_hfield.zy = numpy.zeros(new_hfield.shape)
# new_hfield.sigmae = grid.PlaneBase(new_hfield.shape)
new_hfield.sigmae = new_efield.sigmae
# new_hfield.sigmah = grid.PlaneBase(new_hfield.shape)
new_hfield.sigmah = new_efield.sigmah


for step in range(1,50):
    new_efield.y[149:152,149:152] += float(math.sin(step*math.pi/6.125))
    new_efield = update_efield( new_efield, new_hfield )
    new_hfield.zx[276,150] += float(math.sin(step*math.pi/6.125))/2
    new_hfield.zy[276,150] += float(math.sin(step*math.pi/6.126))/2
    new_hfield = update_hfield( new_efield, new_hfield )

    h = numpy.array(new_hfield.z, dtype="float")
    
    for i in xrange(1,300):
        for j in xrange(1,300):
            if (i+j)%2 == 1:
                h[i,j] = ( h[i+1,j] + h[i-1,j] + h[i,j+1] + h[i,j-1] ) / 4
                
    pylab.imshow( h, interpolation="quadric", norm=matplotlib.colors.Normalize(-0.3,0.3,True) )
    pylab.colorbar()

    pylab.savefig("result/fdtd_plane-%.3d.png" % step)
    pylab.clf()
    print step


if "Darwin" in os.uname():
    os.system("open result")


