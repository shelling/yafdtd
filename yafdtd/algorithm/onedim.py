import math


def update_dfield(string):
    for x in range(1,string.shape[0]):
        string.dfield[x] = string.dfield[x] + 0.5 * ( string.hfield[x-1] - string.hfield[x] )
    return string

def update_efield(string):
    """
    update efield
    
    Arguments:
    - `string`: yafdtd.String instance containing fields and material data
    """
    for x in range(1, string.shape[0]):
        # string.efield[x] = string.efield[x] + 0.5 * ( string.hfield[x-1] - string.hfield[x] )
        string.efield[x] = string.dfield[x]
    return string

def update_bfield(string):
    for x in range(0, string.shape[0]-1):
        string.bfield[x] = string.bfield[x] + 0.5 * ( string.efield[x] - string.efield[x+1] )
    return string

def update_hfield(string):
    """
    update hfield
    
    Arguments:
    - `string`: yafdtd.String instance containing fields and material data
    """
    for x in range(0, string.shape[0]-1):
        string.hfield[x] = string.bfield[x]
        # string.hfield[x] = string.hfield[x] + 0.5 * ( string.efield[x] - string.efield[x+1] )
    return string





def update_abc(string, abc={"lm1":0, "lm2":0, "rm1":0, "rm2":0}):
    """
    update cells of Absorbing Boundary Conditions
    
    Arguments:
    - `string`: yafdtd.String instance containing fields and material data
    - `abc`: static variable stored previous data in two steps, which should not be feed by your own.
    """
    update_abc_left(string)
    update_abc_right(string)
    return None

def update_abc_left(string, abc={"m1":0, "m2":0}):
    """
    update left side cell of Absorbing Boundary Conditions
    
    Arguments:
    - `string`:
    - `abc`:
    """
    string.efield[0] = abc["m2"]
    abc["m2"] = abc["m1"]
    abc["m1"] = string.efield[1]
    return None

def update_abc_right(string, abc={"m1":0, "m2":0}):
    """
    update right side cell of Absorbing Boundary Conditions
    
    Arguments:
    - `string`:
    - `abc`:
    """
    string.efield[-1] = abc["m2"]
    abc["m2"] = abc["m1"]
    abc["m1"] = string.efield[-2]
    return None


