import mpmath
import math

from fdtd import grid

def update_efield( efield, hfield ):
    """
    Two dimension efield update equation

    all points at ( x + y ) % 2 == 1 would be updated.

    Arguments:
    - efield: previous efield
    - hfield: previous hfield
    """
    new_efield = grid.Plane( abuffer=efield )

    (xaxis,yaxis) = efield.x.shape
    
    for i in range(1,xaxis-1):
        for j in range(1,yaxis-1):
            if (i+j)%2 == 1:
                curl_coefficient = (new_efield.timestep / (new_efield.spacestep * new_efield.eps[i,j]))
                new_efield.x[i,j] = efield.x[i,j] + curl_coefficient * ( hfield.z[i,j+1] - hfield.z[i,j-1] )
                new_efield.y[i,j] = efield.y[i,j] - curl_coefficient * ( hfield.z[i+1,j] - hfield.z[i-1,j] )

    return new_efield


def update_hfield( efield, hfield ):
    """
    Two dimension hfield update equation

    all points at ( x + y ) % 2 == 0 would be updated.
    """
    new_hfield = grid.Plane( abuffer=hfield )
    
    (xaxis,yaxis) = hfield.x.shape
    
    for i in range(1,xaxis-1):
        for j in range(1,yaxis-1):
            if (i+j)%2 == 0:
                curl_coefficient = new_hfield.timestep / (new_hfield.spacestep * new_hfield.mu[i,j])
                new_hfield.z[i,j] = hfield.z[i,j] + curl_coefficient * ( efield.x[i,j+1] - efield.x[i,j-1] ) - curl_coefficient * ( efield.y[i+1,j] - efield.y[i-1,j] )
    
    return new_hfield

