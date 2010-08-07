"""
fdtd.grid.py

Implement three kinds of grid object 
String as 1-D grid
Plane as 2-D grid
Cube as 3-D grid

"""

import numpy
from scipy.constants import epsilon_0, mu_0

# {{{
class String(object):
    """
    1-D grid object
    """
    
    def __init__(self, length):
        """
        giving length as quantity of cells to create a FDTD String
        
        Arguments:
        - `length`: quantity of cells
        """
        self.efield = numpy.zeros(length)
        self.hfield = numpy.zeros(length)
        self.eps    = numpy.zeros(length)
        self.sigmae = numpy.zeros(length)
        self.shape  = self.efield.shape
        pass


# }}}



# {{{
class Plane(object):
    """
    Two dimension grid object
    Only generial parameters are defined in constructor.
    The rest, related to BPML or UPML, are appended in helper functions
    """

    def __init__(self, shape, transverse ):
        """
        Arguments:
        - `shape`: specify plance shape
        - `transverse`: TM (Ez Hx Hy) or TE (Hz Ex Ey)
        """

        self.shape = shape
        self.transverse = transverse

        if transverse == "TE":
            self.hzfield = numpy.zeros(shape)
            self.exfield = numpy.zeros(shape)
            self.eyfield = numpy.zeros(shape)
        elif transverse == "TM":
            self.ezfield = numpy.zeros(shape)
            self.hxfield = numpy.zeros(shape)
            self.hyfield = numpy.zeros(shape)
        else:
            # raise error here
            pass

        return None

# }}}

# {{{
class Cube(object):
    """ Three dimension grid object """
    
    def __init__(self, abuffer):
        """
        
        Arguments:
        - `abuffer`:
        """
        self._abuffer = abuffer

# }}}        
        

        
# {{{        
class Point(object):
    """ Grid point object used in grid array """
    
    def __init__(self, properties = {}):
        """
        pass a properties hash to initialize it
        Arguments:
        - `properties`: hash
        """
        self._properties = properties
        self.eps   = properties["eps"]
        self.mu    = properties["mu"]
        self.sigma = properties["sigma"]
        
# }}}

# {{{

class Cylinder(object):
    """
    3-D grid object of coordinate R Phi Z
    """
    
    def __init__(self, shape):
        """
        giving shape contain R Phi Z to create Cylinder
        
        Arguments:
        - `shape`:
        """
        self._shape = shape
        pass


# }}}