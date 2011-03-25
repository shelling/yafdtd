"""
yafdtd.grid.py

Implement three kinds of grid object 
String as 1-D grid
Plane as 2-D grid
Cube as 3-D grid

"""
import matplotlib
import numpy
import pylab

from scipy.constants import epsilon_0, mu_0
from matplotlib import _pylab_helpers, cm
from yafdtd.algorithm import onedim, twodim, threedim
from yafdtd.source import HardSource, TFSF
from yafdtd import utils


class String(object):
    """
    1-D grid object
    """
    
    update_dfield = onedim.update_dfield
    update_efield = onedim.update_efield
    update_bfield = onedim.update_bfield
    update_hfield = onedim.update_hfield

    update_abc = onedim.update_abc
    
    def __init__(self, length):
        """
        giving length as quantity of cells to create a FDTD String
        
        Arguments:
        - `length`: quantity of cells
        """
        self.dfield = numpy.zeros(length)
        self.efield = numpy.zeros(length)
        self.bfield = numpy.zeros(length)
        self.hfield = numpy.zeros(length)
        self.eps    = numpy.zeros(length)
        self.sigmae = numpy.zeros(length)
        self.shape  = self.efield.shape
        return None

    def curl_e(self):
        return numpy.array([self.efield[x] - self.efield[x+1] for x in range(self.shape[0]-1)] + [0])

    def curl_h(self):
        return numpy.array([0] + [self.hfield[x-1] - self.hfield[x] for x in range(1, self.shape[0])])

    def update_source(self, t):
        """
        write the new value of source into problem region
        
        Arguments:
        - `t`: current timestep
        """
        if isinstance(self.source, HardSource):
            self.efield[self.source.position] = self.source.function(t, *(self.source.options))
        elif isinstance(self.source, TFSF):
            # not yet implement
            pass
        return self


    def plot(self, pattern, id, intensity=[-1,1]):
        """
        plot the String instance to a file
        
        Arguments:
        - `pattern`: filename pattern
        """
        utils.plot(self.efield, pattern, id, intensity)
        return None



class Plane(object):
    """
    Two dimension grid object
    Only generial parameters are defined in constructor.
    The rest, related to BPML or UPML, are appended in helper functions
    """
    update_dfield = twodim.freespace.update_dfield
    update_efield = twodim.freespace.update_efield
    update_bfield = twodim.freespace.update_bfield
    update_hfield = twodim.freespace.update_hfield

    def __init__(self, shape):
        """
        Arguments:
        - `shape`: specify plance shape
        - `transverse`: TM (Ez Hx Hy) or TE (Hz Ex Ey)
        """

        self.shape = shape
        
        self.dxfield = numpy.zeros(shape)
        self.dyfield = numpy.zeros(shape)
        self.dzfield = numpy.zeros(shape)

        self.exfield = numpy.zeros(shape)
        self.eyfield = numpy.zeros(shape)
        self.ezfield = numpy.zeros(shape)

        self.bxfield = numpy.zeros(shape)
        self.byfield = numpy.zeros(shape)
        self.bzfield = numpy.zeros(shape)

        self.hxfield = numpy.zeros(shape)
        self.hyfield = numpy.zeros(shape)
        self.hzfield = numpy.zeros(shape)

        return None

    def curl_ex(self):
        res = numpy.zeros(self.shape)
        (x,y) = self.shape
        for i in range(x):
            for j in range(y-1):
                res[i,j] = self.ezfield[i,j+1] - self.ezfield[i,j]
        for i in range(x):
            res[i,y-1] = self.ezfield[i,0] - self.ezfield[i,y-1]
        return res

    def curl_ey(self):
        res = numpy.zeros(self.shape)
        (x,y) = self.shape
        for i in range(x-1):
            for j in range(y):
                res[i,j] =-self.ezfield[i+1,j] + self.ezfield[i,j]
        for j in range(y):
            res[x-1,j] =-self.ezfield[0,j] + self.ezfield[x-1,j]
        return res

    def curl_ez(self):
        res = numpy.zeros(self.shape)
        (x,y) = self.shape
        for i in range(x-1):
            for j in range(y-1):
                res[i,j] = self.eyfield[i+1,j] - self.eyfield[i,j] - self.exfield[i,j+1] + self.exfield[i,j]
        for i in range(x-1):
            res[i,y-1] = self.eyfield[i+1,y-1] - self.eyfield[i,y-1] - self.exfield[i,0] + self.exfield[i,y-1]
        for j in range(y-1):
            res[x-1,j] = self.eyfield[0,j] - self.eyfield[x-1,j] - self.exfield[x-1,j+1] + self.exfield[x-1,j]
        res[x-1,y-1] = self.eyfield[0,y-1] - self.eyfield[x-1,y-1] - self.exfield[x-1,0] + self.exfield[x-1,y-1]
        return res
    
    def curl_hx(self):
        """
        for TEz case
        """
        res = numpy.zeros(self.shape)
        (x,y) = self.shape
        for i in range(x):
            for j in range(1,y):
                res[i,j] = self.hzfield[i,j] - self.hzfield[i,j-1]
        for i in range(x):
            res[i,0] = self.hzfield[i,0] - self.hzfield[i,y-1]
        return res

    def curl_hy(self):
        """
        for TEz case
        """
        res = numpy.zeros(self.shape)
        (x,y) = self.shape
        for i in range(1,x):
            for j in range(y):
                res[i,j] =-self.hzfield[i,j] + self.hzfield[i-1,j]
        for j in range(y):
            res[0,j] =-self.hzfield[0,j] + self.hzfield[x-1,j]
        return res

    def curl_hz(self):
        """
        for TMz case
        """
        res = numpy.zeros(self.shape)
        (x,y) = self.shape
        for i in range(1,x):
            for j in range(1,y):
                res[i,j] = self.hyfield[i,j] - self.hyfield[i-1,j] - self.hxfield[i,j] + self.hxfield[i,j-1]
        for i in range(1,x):
            res[i,0] = self.hyfield[i,0] - self.hyfield[i-1,0] - self.hxfield[i,0] + self.hxfield[i,y-1]
        for j in range(1,y):
            res[0,j] = self.hyfield[0,j] - self.hyfield[x-1,j] - self.hxfield[0,j] + self.hxfield[0,j-1]
        res[0,0] = self.hyfield[0,0] - self.hyfield[x-1,0] - self.hxfield[0,0] + self.hxfield[0,y-1]
        return res


class Cube(object):
    """ Three dimension grid object """

    update_dfield = threedim.freespace.update_dfield
    update_efield = threedim.freespace.update_efield
    update_bfield = threedim.freespace.update_bfield
    update_hfield = threedim.freespace.update_hfield
    
    def __init__(self, shape):
        """
        
        Arguments:
        - `abuffer`:
        """
        self.shape = shape
        
        self.dxfield = numpy.zeros(shape)
        self.dyfield = numpy.zeros(shape)
        self.dzfield = numpy.zeros(shape)
        
        self.exfield = numpy.zeros(shape)
        self.eyfield = numpy.zeros(shape)
        self.ezfield = numpy.zeros(shape)

        self.bxfield = numpy.zeros(shape)
        self.byfield = numpy.zeros(shape)
        self.bzfield = numpy.zeros(shape)
        
        self.hxfield = numpy.zeros(shape)
        self.hyfield = numpy.zeros(shape)
        self.hzfield = numpy.zeros(shape)
        
        return None

    def curl_ex(self):
        res = numpy.zeros(self.shape)
        (x,y,z) = self.shape
        for i in range(x):
            for j in range(y-1):
                for k in range(z-1):
                    res[i,j,k] = self.ezfield[i,j+1,k] - self.ezfield[i,j,k] - self.eyfield[i,j,k+1] + self.eyfield[i,j,k]
        return res

    def curl_ey(self):
        res = numpy.zeros(self.shape)
        (x,y,z) = self.shape
        for i in range(x-1):
            for j in range(y):
                for k in range(z-1):
                    res[i,j,k] = self.exfield[i,j,k+1] - self.exfield[i,j,k] - self.ezfield[i+1,j,k] + self.ezfield[i,j,k]
        return res

    def curl_ez(self):
        res = numpy.zeros(self.shape)
        (x,y,z) = self.shape
        for i in range(x-1):
            for j in range(y-1):
                for k in range(z):
                    res[i,j,k] = self.eyfield[i+1,j,k] - self.eyfield[i,j,k] - self.exfield[i,j+1,k] + self.exfield[i,j,k]
        return res

    def curl_hx(self):
        res = numpy.zeros(self.shape)
        (x,y,z) = self.shape
        for i in range(x):
            for j in range(y):
                for k in range(z):
                    res[i,j,k] = self.hzfield[i,j,k] - self.hzfield[i,j-1,k] - self.hyfield[i,j,k] + self.hyfield[i,j,k-1]
        return res

    def curl_hy(self):
        res = numpy.zeros(self.shape)
        (x,y,z) = self.shape
        for i in range(x):
            for j in range(y):
                for k in range(z):
                    res[i,j,k] = self.hxfield[i,j,k] - self.hxfield[i,j,k-1] - self.hzfield[i,j,k] + self.hzfield[i-1,j,k]
        return res

    def curl_hz(self):
        res = numpy.zeros(self.shape)
        (x,y,z) = self.shape
        for i in range(x):
            for j in range(y):
                for k in range(z):
                    res[i,j,k] = self.hyfield[i,j,k] - self.hyfield[i-1,j,k] - self.hxfield[i,j,k] + self.hxfield[i,j-1,k]
        return res

        
