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


# {{{
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

    def update_source(self, t):
        """
        write the new value of source into problem region
        
        Arguments:
        - `t`: current timestep
        """
        if type(self.source) == HardSource:
            self.efield[self.source.position] = self.source.function(t, *(self.source.options))
        elif type(self.source) == TFSF:
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
        
        self.ga = numpy.ones(shape)
        self.gb = numpy.zeros(shape)

        if transverse == "TE":
            self.dxfield = numpy.zeros(shape)
            self.dyfield = numpy.zeros(shape)
            
            self.exfield = numpy.zeros(shape)
            self.eyfield = numpy.zeros(shape)
            
            self.bzfield = numpy.zeros(shape)
            
            self.hzfield = numpy.zeros(shape)
        elif transverse == "TM":
            self.dzfield = numpy.zeros(shape)

            self.ezfield = numpy.zeros(shape)

            self.bxfield = numpy.zeros(shape)
            self.byfield = numpy.zeros(shape)
            
            self.hxfield = numpy.zeros(shape)
            self.hyfield = numpy.zeros(shape)
            
            self.ihx     = numpy.zeros(shape)
            self.ihy     = numpy.zeros(shape)
        else:
            # raise error here
            pass

        return None

    def append(self, object):
        """
        append extra object onto the Plane instance.
        The object can be a instance of PML, Geometry, Source, etc.
        
        Arguments:
        - `object`:
        """
        object.stick(self)
        return self


    def update_efield(self):
        """
        update efield of the Plane instance
        """
        if type(self.pml) == twodim.upml.UPML:
            twodim.upml.update_efield(self)
        elif type(self.pml) == twodim.bpml.BPML:
            # not yet implement
            pass
        return self

    def update_hfield(self):
        """
        update hfield of the Plane instance
        """
        if type(self.pml) == twodim.upml.UPML:
            twodim.upml.update_hfield(self)
        elif type(self.pml) == twodim.bpml.BPML:
            # not yet implement
            pass
        return self



    def update_source(self, t):
        """
        write the new value of souce into auxiliary
        
        Arguments:
        - `t`:
        """
        if type(self.source) == HardSource:
            self.ezfield[self.source.position] = self.source.function(t, *(self.source.options))
        elif type(self.source) == TFSF:
            length    = self.source.length
            edge      = self.source.thick
            auxiliary = self.source.auxiliary
            auxiliary.update_efield().update_abc().update_source(t)
            for i in range(edge,length-edge):
                self.dzfield[i,edge]        = self.dzfield[i,edge]        + 0.5 * auxiliary.hfield[edge-1]
                self.dzfield[i,length-edge] = self.dzfield[i,length-edge] - 0.5 * auxiliary.hfield[length-edge]
            auxiliary.update_hfield()
            for i in range(edge,length-edge):
                self.hxfield[i,edge-1]      = self.hxfield[i,edge-1]      + 0.5 * auxiliary.efield[edge]
                self.hxfield[i,length-edge] = self.hxfield[i,length-edge] - 0.5 * auxiliary.efield[length-edge]
            for j in range(edge,length-edge):
                self.hyfield[edge-1,j]      = self.hyfield[edge-1,j]      - 0.5 * auxiliary.efield[j]
                self.hyfield[length-edge,j] = self.hyfield[length-edge,j] + 0.5 * auxiliary.efield[j]
        return self

    def plot(self, pattern, id, range=[-1,1]):
        """
        plot the Plane instance to a file of 2-D view
        
        Arguments:
        - `pattern`:
        - `id`:
        - `range`:
        """
        fig = pylab.figure()
        if self.transverse == "TM":
            field = self.ezfield
        elif self.transverse == "TE":
            field = self.hzfield
        im = fig.gca().imshow( field, norm=matplotlib.colors.Normalize( *(range + [True]) ) )
        fig.colorbar(im)
        fig.savefig(pattern % id)
        _pylab_helpers.Gcf.destroy_fig(fig)
        return self
    def plot3d(self, pattern, id, range=[-1,1]):
        """
        plot the Plane instance to a file of 3-D view
        
        Arguments:
        - `pattern`:
        - `id`:
        - `range`:
        """
        if self.transverse == "TM":
            field = self.ezfield
        elif self.transverse == "TE":
            field = self.hzfield

        x = numpy.arange(0, self.shape[0])
        y = numpy.arange(0, self.shape[1])
        x, y = numpy.meshgrid(x, y)
        fig = pylab.figure()
        ax = fig.gca(projection="3d")
        ax.plot_surface(x, y, field, rstride=1, cstride=1, cmap=cm.jet, linewidth=0, antialiased=False, norm=matplotlib.colors.Normalize(-1,1,True))
        ax.set_zlim3d(range)
        fig.savefig(pattern % id)
        _pylab_helpers.Gcf.destroy_fig(fig)
        return self


# }}}

# {{{
class Cube(object):
    """ Three dimension grid object """
    
    def __init__(self, shape):
        """
        
        Arguments:
        - `abuffer`:
        """
        self._abuffer = abuffer
        
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
