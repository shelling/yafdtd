from numpy import *

class OneDim(ndarray):
    """ ONE dimension grid object """
    
    def __init__(self, *args):
        """
        """
        pass
        
# {{{
class Plane(ndarray):
    """ Two dimension grid object """

    def __new__(cls, abuffer=None):
        abuffer = array(abuffer, dtype="float128")
        print abuffer
        if len(abuffer.shape) == 2:
            return ndarray.__new__(cls, abuffer.shape, "float128", abuffer)
        else:
            # TODO:
            # should raise an error here
            pass

    def __init__(self, abuffer):
        """ 
        Arguments:
        - `abuffer`:
        """
        pass
# }}}
        
        
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
        
