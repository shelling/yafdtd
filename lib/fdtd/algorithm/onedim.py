import math
import mpmath


def update_efield(string):
    """
    update efield
    
    Arguments:
    - `string`: fdtd.String instance containing fields and material data
    """
    for x in range(1, string.shape[0]-1):
        string.efield[x] = string.efield[x] + 0.5 * ( string.hfield[x-1] - string.hfield[x] )
    return None





def update_hfield(string):
    """
    update hfield
    
    Arguments:
    - `string`: fdtd.String instance containing fields and material data
    """
    for x in range(0, string.shape[0]-1):
        string.hfield[x] = string.hfield[x] + 0.5 * ( string.efield[x] - string.efield[x+1] )
    return None





def update_abc(string, abc={"lm1":0, "lm2":0, "rm1":0, "rm2":0}):
    """
    update cells of Absorbing Boundary Conditions
    
    Arguments:
    - `string`: fdtd.String instance containing fields and material data
    - `abc`: static variable stored previous data in two steps, which should not be feed by your own.
    """
    # left-hand side
    string.efield[0]  = abc["lm2"]
    abc["lm2"] = abc["lm1"]
    abc["lm1"] = string.efield[1]
    # right-hand side
    string.efield[string.shape[0]-1] = abc["rm2"]
    abc["rm2"] = abc["rm1"]
    abc["rm1"] = string.efield[string.efield.shape[0]-2]
    return None




def update_source(string, locate, source, params):
    """
    update source intensity on fdtd.String instance
    
    Arguments:
    - `string`: fdtd.String instance containing fields and material data
    - `locate`: the position where source would update
    - `source`: source function
    - `params`: array containing parameters would be passed to source
    """
    string.efield[locate] = apply(source, params)
    return None
