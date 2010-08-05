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
class String():
    """
    1-D grid 
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
    """

    def __init__(self, abuffer=None, shape=None, eps=epsilon_0, mu=mu_0, sigmae=0, sigmah=0, timestep=None, spacestep=None):
        """
        Give one of shape or abuffer to initialize Plane object.
        
        Once abuffer is given, shape and other parameters would be obsolete.

        Alternatively, if abuffer is None, Plane would be initialized with rest parameters.

        If both abuffer and shape were not given, Error would be raised.
        
        Arguments:
        - abuffer: grid buffer used to initialize plane
        - shape: specify plance shape
        - eps: primary permitivity value would be assign to whole region
        - mu: primary permeability value would be assign to whole region
        - sigmae: primary lossy coefficient of E field
        - sigmah: primary lossy coefficient of H field
        """
        if abuffer and len(abuffer.x.shape) == 2:
            self.shape  = abuffer.x.shape
            
            self.x      = numpy.zeros_like(abuffer.x)
            self.y      = numpy.zeros_like(abuffer.y)
            self.z      = numpy.zeros_like(abuffer.z)
            
            self.eps    = abuffer.eps
            self.mu     = abuffer.mu
            self.sigmae = abuffer.sigmae
            self.sigmah = abuffer.sigmah
            
            self.timestep  = abuffer.timestep
            self.spacestep = abuffer.spacestep
            
        elif shape and len(shape) == 2:
            self.shape  = shape
            self.x      = numpy.zeros(shape, dtype="float128")
            self.y      = numpy.zeros(shape, dtype="float128")
            self.z      = numpy.zeros(shape, dtype="float128")
            
            self.eps    = numpy.ndarray(shape=self.x.shape, dtype="float128"); self.eps[0:,0:] = eps
            self.mu     = numpy.ndarray(shape=self.x.shape, dtype="float128"); self.mu[0:,0:]  = mu
            self.sigmae = numpy.ndarray(shape=self.x.shape, dtype="float128"); self.sigmae[0:,0:] = sigmae
            self.sigmah = numpy.ndarray(shape=self.x.shape, dtype="float128"); self.sigmah[0:,0:] = sigmah
            
            self.timestep  = (timestep or 1)
            self.spacestep = (spacestep or 1)
        pass

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

class PlaneBase(object):
    """
    Base plane object, just be able to store (x,y,z) value at every points in an array.

    This class aims to become base class of that need to store field corresponding parameters.
    
    """
    
    def __init__(self, shape=None, abuffer=None):
        """
        
        Arguments:
        - `shape`:
        - `abuffer`:
        """
        if abuffer:
            self.shape = abuffer.shape
            self.x     = abuffer.x
            self.y     = abuffer.y
            self.z     = abuffer.z
            
        elif len(shape) == 2 and isinstance(shape,type(tuple())):
            self.shape = shape
            self.x     = numpy.zeros(shape)
            self.y     = numpy.zeros(shape)
            self.z     = numpy.zeros(shape)
        pass

# }}}
