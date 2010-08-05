from mpmath import *


def update_efield(efield, hfield):
    """
    update efield
    
    Arguments:
    - `efield`:
    """
    for x in range(1, efield.shape[0]-1):
        efield[x] = efield[x] + 0.5 * ( hfield[x-1] - hfield[x] )


def update_hfield(efield, hfield):
    """
    update hfield
    
    Arguments:
    - `efield`:
    - `hfield`:
    """
    for x in range(0, hfield.shape[0]-1):
        hfield[x] = hfield[x] + 0.5 * ( efield[x] - efield[x+1] )
