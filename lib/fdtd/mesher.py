from numpy import *
from fdtd import grid

def line(abuffer):
    """
    
    Arguments:
    - `abuffer`:
    """
    return grid.Line(abuffer)
    

def plane(abuffer):
    """
    
    Arguments:
    - `abuffer`:
    """
    return grid.Plane(abuffer)

def cube(abuffer):
    """
    
    Arguments:
    - `abuffer`:
    """
    return grid.Cube(abuffer)

