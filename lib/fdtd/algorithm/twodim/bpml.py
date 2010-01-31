import mpmath
import math

from fdtd import grid

def update_efield( efield, hfield, region=None ):
    """
    """
    new_efield = grid.Plane( abuffer = efield )
    (xaxis,yaxis) = efield.x.shape
    for i in range(1,xaxis-1):
        for j in range(1,yaxis-1):
            if (i+j)%2 == 1:
                pass
    return new_efield


def update_hfield( efield, hfield, region=None ):
    """
    """
    new_hfield = grid.Plane( abuffer = hfield )
    return new_hfield
