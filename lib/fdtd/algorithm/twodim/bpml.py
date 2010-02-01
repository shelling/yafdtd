import mpmath
import math
import numpy

from fdtd import grid


def update_efield( efield, hfield, region=None ):
    """
    2-D E field update eqution upon BPML

    using region to specify work region, or work on whole region
    """
    new_efield = grid.Plane( abuffer = efield )

    (xaxis,yaxis) = efield.x.shape
    
    for i in range(1,xaxis-1):
        for j in range(1,yaxis-1):
            if (i+j)%2 == 1:
                cx  = 0.5 * efield.sigmae.y[i,j] * efield.timestep
                cax = ( efield.eps[i,j] - cx ) / ( efield.eps[i,j] + cx )
                cbx = efield.timestep / ( efield.spacestep * ( efield.eps[i,j] + cx ) )
                new_efield.x[i,j] = cax * efield.x[i,j] + cbx * ( hfield.z[i,j+1] - hfield.z[i,j-1] )

                cy  = 0.5 * efield.sigmae.x[i,j] * efield.timestep
                cay = ( efield.eps[i,j] - cy ) / ( efield.eps[i,j] + cy )
                cby = efield.timestep / ( efield.spacestep * ( efield.eps[i,j] + cy ) )
                new_efield.y[i,j] = cay * efield.y[i,j] - cby * ( hfield.z[i+1,j] - hfield.z[i-1,j] )
    return new_efield


def update_hfield( efield, hfield, region=None ):
    """
    2-D H field update equation upon BPML

    using region to specify work region, or work on whole region
    """
    new_hfield = grid.Plane( abuffer = hfield )

    new_hfield.zx = numpy.zeros(new_hfield.shape) # append zx and zy component
    new_hfield.zy = numpy.zeros(new_hfield.shape) # of H field for succeeding calculation

    (xaxis,yaxis) = hfield.shape

    for i in xrange(1,xaxis-1):
        for j in xrange(1,yaxis-1):
            if (i+j)%2 == 0:
                dx   = 0.5 * hfield.sigmah.x[i,j]
                dazx = ( hfield.mu[i,j] - dx ) / ( hfield.mu[i,j] + dx )
                dbzx = hfield.timestep / ( hfield.spacestep * ( hfield.mu[i,j] + dx ) )
                new_hfield.zx[i,j] = dazx * hfield.zx[i,j] - dbzx * ( efield.y[i+1,j] - efield.y[i-1,j] )
                
                dy   = 0.5 * hfield.sigmah.y[i,j]
                dazy = ( hfield.mu[i,j] - dy ) / ( hfield.mu[i,j] + dy )
                dbzy = hfield.timestep / ( hfield.spacestep * ( hfield.mu[i,j] + dy ) )
                new_hfield.zy[i,j] = dazy * hfield.zy[i,j] + dbzy * ( efield.x[i,j+1] - efield.x[i,j-1] )
                
    new_hfield.z = new_hfield.zx + new_hfield.zy

    return new_hfield


