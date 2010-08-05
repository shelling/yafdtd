import math
import mpmath


def update_efield(string):
    """
    update efield
    
    Arguments:
    - `string`: FDTD.String object containing fields and material data
    """
    for x in range(1, string.shape[0]-1):
        string.efield[x] = string.efield[x] + 0.5 * ( string.hfield[x-1] - string.hfield[x] )


def update_hfield(string):
    """
    update hfield
    
    Arguments:
    - `string`: FDTD.String instance containing fields and material data
    """
    for x in range(0, string.shape[0]-1):
        string.hfield[x] = string.hfield[x] + 0.5 * ( string.efield[x] - string.efield[x+1] )
