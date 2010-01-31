"""
fdtd.grid.py

Implement three kinds of grid object 
Line as 1-D grid
Plane as 2-D grid
Cube as 3-D grid

"""

import numpy
from scipy.constants import epsilon_0, mu_0

# {{{
class Line(object):
    """
    One dimension grid object
    """
    
    def __init__(self, step = {}):
        """
        """
        
    def timestep(self, ):
        """
        """
# }}}        


# {{{
class Plane(object):
    """
    Two dimension grid object
    """

    def __init__(self, abuffer=None, shape=None, eps=None, mu=None, sigmae=None, sigmah=None, timestep=None, spacestep=None):
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
            self.x      = numpy.zeros_like(abuffer.x)
            self.y      = numpy.zeros_like(abuffer.y)
            self.z      = numpy.zeros_like(abuffer.z)
            
            self.eps    = abuffer.eps
            self.mu     = abuffer.mu
            self.sigmae = abuffer.sigmae
            self.sigmah = abuffer.sigmah
            
            self.timestep  = abuffer.timestep
            self.spacestep = abuffer.spacestep
            
        elif shape:
            self.x      = numpy.zeros(shape, dtype="float128")
            self.y      = numpy.zeros(shape, dtype="float128")
            self.z      = numpy.zeros(shape, dtype="float128")
            
            self.eps    = numpy.ndarray(shape=self.x.shape, dtype="float128"); self.eps[0:,0:] = (eps or epsilon_0)
            self.mu     = numpy.ndarray(shape=self.x.shape, dtype="float128"); self.mu[0:,0:]  = (mu or mu_0)
            self.sigmae = numpy.ndarray(shape=self.x.shape, dtype="float128"); self.sigmae[0:,0:] = (sigmae or 0)
            self.sigmah = numpy.ndarray(shape=self.x.shape, dtype="float128"); self.sigmah[0:,0:] = (sigmah or 0)
            
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
