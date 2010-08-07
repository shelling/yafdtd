import mpmath
import math


def update_efield( plane ):
    """
    Two dimension efield update equation

    Arguments:
    - `plane`: fdtd.grid.Plane instance 
    """
    (xaxis,yaxis) = plane.shape

    if plane.transverse == "TE":
        for i in range(1,xaxis):
            for j in range(1,yaxis):
                plane.exfield[i,j] = plane.exfield[i,j] + 0.5 * ( plane.hzfield[i,j+1] - plane.hzfield[i,j-1] )
                plane.eyfield[i,j] = plane.eyfield[i,j] - 0.5 * ( plane.hzfield[i+1,j] - plane.hzfield[i-1,j] )
    elif plane.transverse == "TM":
        for i in range(0,xaxis):
            for j in range(0,yaxis):
                plane.ezfield[i,j] = plane.ezfield[i,j] + 0.5 * ( plane.hyfield[i,j] - plane.hyfield[i-1,j] - plane.hxfield[i,j] + plane.hxfield[i,j-1] )
    return None


def update_hfield( plane ):
    """
    Two dimension hfield update equation
    
    Arguments:
    - `plane`: fdtd.grid.Plane instance 
    """
    (xaxis,yaxis) = plane.shape

    if plane.transverse == "TE":
        for i in range(0,xaxis-1):
            for j in range(0,yaxis-1):
                plane.hzfield[i,j] = plane.hzfield[i,j] + 0.5 * ( plane.exfield[i,j+1] - plane.exfield[i,j-1] ) - 0.5 * ( plane.eyfield[i+1,j] - plane.eyfield[i-1,j] )
    elif plane.transverse == "TM":
        for i in range(0,xaxis-1):
            for j in range(0,yaxis-1):
                plane.hxfield[i,j] = plane.hxfield[i,j] + 0.5 * ( plane.ezfield[i,j] - plane.ezfield[i,j+1] )
                plane.hyfield[i,j] = plane.hyfield[i,j] + 0.5 * ( plane.ezfield[i+1,j] - plane.ezfield[i,j] )
    return None

