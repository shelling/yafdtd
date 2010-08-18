from numpy import *
from fdtd import grid

def string(length):
    """
    
    Arguments:
    - `length`: how many meters the grid holds
    - ``:
    """
    return grid.String()
    

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

