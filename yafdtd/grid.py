"""
yafdtd.grid.py

Implement three kinds of grid object 
String as 1-D grid
Plane as 2-D grid
Cube as 3-D grid

"""
import numpy, h5py

from scipy.constants import c
from yafdtd import utils
from yafdtd.geometry import circle, rectangle
from yafdtd.geometry import twodim


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
        self.shape  = (length,)
        
        self.dfield = numpy.zeros(length)
        self.efield = numpy.zeros(length)
        self.bfield = numpy.zeros(length)
        self.hfield = numpy.zeros(length)

        return None

    def update_dfield(string):
        string.dfield += 0.5 * string.curl_h()
        return string

    def update_efield(string):
        """
        update efield
        """
        string.efield = string.dfield.copy()
        return string

    def update_bfield(string):
        """
        update bfield
        """
        string.bfield += 0.5 * string.curl_e()
        return string

    def update_hfield(string):
        """
        update hfield
        """
        string.hfield = string.bfield.copy()
        return string


    def update_abc(self, abc={"lm1":0, "lm2":0, "rm1":0, "rm2":0}):
        """
        update cells of Absorbing Boundary Conditions
        """
        self.update_abc_left()
        self.update_abc_right()
        return self

    def update_abc_left(self, abc={"m1":0, "m2":0}):
        self.efield[0] = abc["m2"]
        abc["m2"] = abc["m1"]
        abc["m1"] = self.efield[1]
        return None

    def update_abc_right(self, abc={"m1":0, "m2":0}):
        self.efield[-1] = abc["m2"]
        abc["m2"] = abc["m1"]
        abc["m1"] = self.efield[-2]
        return None

    def curl_e(self):
        return numpy.array([self.efield[x] - self.efield[x+1] for x in range(self.shape[0]-1)] + [0])

    def curl_h(self):
        return numpy.array([0] + [self.hfield[x-1] - self.hfield[x] for x in range(1, self.shape[0])])

    def update_source(self, source):
        """ insert value into self.dfield[self.enter] """
        self.dfield[self.enter] = source
        return self

    def update(self, source):
        self.update_dfield()
        self.update_source(source)
        self.update_efield()
        self.update_abc()
        self.update_bfield()
        self.update_hfield()
        return self

    def plot_e(self, name):
        utils.plot(self.efield, name)
        return self

    def plot_h():
        utils.plot(self,hfield, name)
        return self

    def inspect(self):
        result = ""
        for item in [
            self.dfield,
            self.efield,
            self.bfield,
            self.hfield
            ]:
            result += str(item.round(2)) + "\n"
        return result

class Plane(object):
    """
    Two dimension grid object
    Only generial parameters are defined in constructor.
    The rest, related to BPML or UPML, are appended in helper functions
    """

    def __init__(self, name, shape):
        """
        Arguments:
        - `shape`: specify plance shape
        """
        self.name = name

        self.shape = shape

        self.attrs = {}
        
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

        # TM edge
        self.hxedgey = numpy.zeros(shape[0])
        self.hyedgex = numpy.zeros(shape[1])
        self.ezedgey = numpy.zeros(shape[0])
        self.ezedgex = numpy.zeros(shape[1])

        # TE edge
        self.exedgey = numpy.zeros(shape[0])
        self.eyedgex = numpy.zeros(shape[1])
        self.hzedgey = numpy.zeros(shape[0])
        self.hzedgex = numpy.zeros(shape[1])

        return None
    
    def update_dfield(self):
        """
        """
        self.dxfield += 0.5 * self.curl_hx()
        self.dyfield += 0.5 * self.curl_hy()
        self.dzfield += 0.5 * self.curl_hz()
        return self

    def update_efield(self):
        """
        """
        self.exfield = self.dxfield.copy()
        self.eyfield = self.dyfield.copy()
        self.ezfield = self.dzfield.copy()
        return self

    def update_bfield(self):
        """
        """
        self.bxfield -= 0.5 * self.curl_ex()
        self.byfield -= 0.5 * self.curl_ey()
        self.bzfield -= 0.5 * self.curl_ez()
        return self

    def update_hfield(self):
        """
        """
        self.hxfield = self.bxfield.copy()
        self.hyfield = self.byfield.copy()
        self.hzfield = self.bzfield.copy()
        return self

    def curl_ex(self):
        res = numpy.zeros(self.shape)
        (x,y) = self.shape
        for i in range(x):
            for j in range(y-1):
                res[i,j] = self.ezfield[i,j+1] - self.ezfield[i,j]
        for i in range(x):
            res[i,y-1] = self.ezedgey[i] - self.ezfield[i,y-1]
        return res

    def curl_ey(self):
        res = numpy.zeros(self.shape)
        (x,y) = self.shape
        for i in range(x-1):
            for j in range(y):
                res[i,j] =-self.ezfield[i+1,j] + self.ezfield[i,j]
        for j in range(y):
            res[x-1,j] =-self.ezedgex[j] + self.ezfield[x-1,j]
        return res

    def curl_ez(self):
        res = numpy.zeros(self.shape)
        (x,y) = self.shape
        for i in range(x-1):
            for j in range(y-1):
                res[i,j] = self.eyfield[i+1,j] - self.eyfield[i,j] - self.exfield[i,j+1] + self.exfield[i,j]
        for i in range(x-1):
            res[i,y-1] = self.eyfield[i+1,y-1] - self.eyfield[i,y-1] - self.exedgey[i] + self.exfield[i,y-1]
        for j in range(y-1):
            res[x-1,j] = self.eyedgex[j] - self.eyfield[x-1,j] - self.exfield[x-1,j+1] + self.exfield[x-1,j]
        res[x-1,y-1] = self.eyedgex[y-1] - self.eyfield[x-1,y-1] - self.exedgey[x-1] + self.exfield[x-1,y-1]
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
            res[i,0] = self.hzfield[i,0] - self.hzedgey[i]
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
            res[0,j] =-self.hzfield[0,j] + self.hzedgex[j]
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
            res[i,0] = self.hyfield[i,0] - self.hyfield[i-1,0] - self.hxfield[i,0] + self.hxedgey[i]
        for j in range(1,y):
            res[0,j] = self.hyfield[0,j] - self.hyedgex[j] - self.hxfield[0,j] + self.hxfield[0,j-1]
        res[0,0] = self.hyfield[0,0] - self.hyedgex[0] - self.hxfield[0,0] + self.hxedgey[0]
        return res

    def imshow_ex(self, name):
        utils.imshow(self.exfield, name)
        return self

    def imshow_ey(self, name):
        utils.imshow(self.eyfield, name)
        return self

    def imshow_ez(self, name):
        utils.imshow(self.ezfield, name)
        return self

    def imshow_hx(self, name):
        utils.imshow(self.hxfield, name)
        return self

    def imshow_hy(self, name):
        utils.imshow(self.hyfield, name)
        return self

    def imshow_hz(self, name):
        utils.imshow(self.hzfield, name)
        return self

    def open(self, filename=None):
        if filename == None:
            filename = "%s.hdf5" % self.name
        self.hdf5 = h5py.File(filename, "w")
        self.hdf5.require_group("timeline")
        return self

    def close(self):
        self.hdf5.close()
        return self

    def save(self):
        self.hdf5.require_group("timeline/%d" % self.t)
        self.hdf5["timeline/%d/ex" % self.t] = self.exfield
        self.hdf5["timeline/%d/ey" % self.t] = self.eyfield
        self.hdf5["timeline/%d/ez" % self.t] = self.ezfield
        self.hdf5["timeline/%d/hx" % self.t] = self.hxfield
        self.hdf5["timeline/%d/hy" % self.t] = self.hyfield
        self.hdf5["timeline/%d/hz" % self.t] = self.hzfield
        return self

    def save_attrs(self):
        self.hdf5.attrs["name"] = self.name
        for (key, value) in self.attrs.items():
            self.hdf5.attrs[key] = value
        return self

    def dx(self, dx):
        self.attrs["dx"] = dx
        self.attrs["dt"] = dx/(2*c)
        return self

    def frequency(self, frequency):
        self.attrs["frequency"]  = frequency
        self.attrs["wavelength"] = c/frequency
        return self

    def wavelength(self, wavelength):
        self.attrs["wavelength"] = wavelength
        self.attrs["frequency"]  = c/wavelength
        return self

    def inspect(self):
        result = ""
        for item in [
            self.dxfield,
            self.dyfield,
            self.dzfield,
            self.exfield,
            self.eyfield,
            self.ezfield,
            self.bxfield,
            self.byfield,
            self.bzfield,
            self.hxfield,
            self.hyfield,
            self.hzfield
            ]:
            result += str(item.round(2)) + "\n"
        return result

class PlaneDecorator(Plane):
    def __init__(self, orig):
        self.__dict__ = orig.__dict__
        if orig.__class__ != Plane:
            self.__class__.__bases__ = (orig.__class__,)
        return None

class PBCPlane(PlaneDecorator):
    def __init__(self, orig):
        super(PBCPlane, self).__init__(orig)
        self.pbcx = True
        self.pbcy = True
        return None

    def pbc(self, x=True, y=True):
        self.pbcx = x
        self.pbcy = y
        return self

    def update_epbc(self, ezedgex=None, eyedgex=None, ezedgey=None, exedgey=None):
        """
        """
        if self.pbcx:
            self.ezedgex = self.ezfield[0,:] # pbc x, TM
            self.eyedgex = self.eyfield[0,:] # pbc x, TE
        if isinstance(ezedgex, numpy.ndarray):
            self.ezedgex = ezedgex           # pbc x, TM, custom
        if isinstance(eyedgex, numpy.ndarray):
            self.eyedgex = eyedgex           # pbc x, TE, custom

        if self.pbcy:
            self.ezedgey = self.ezfield[:,0] # pbc y, TM
            self.exedgey = self.exfield[:,0] # pbc y, TE
        if isinstance(ezedgey, numpy.ndarray):
            self.ezedgey = ezedgey           # pbc y, TM, custom
        if isinstance(exedgey, numpy.ndarray):
            self.exedgey = exedgey           # pbc y, TE, custom
        return self

    def update_hpbc(self, hyedgex=None, hzedgex=None, hxedgey=None, hzedgey=None):
        """
        """
        xmax = self.shape[0]-1
        ymax = self.shape[1]-1
        if self.pbcx:
            self.hyedgex = self.hyfield[xmax,:] # pbc x, TM
            self.hzedgex = self.hzfield[xmax,:] # pbc x, TE
        if isinstance(hyedgex, numpy.ndarray):
            self.hyedgex = hyedgex              # pbc x, TM, custom
        if isinstance(hzedgex, numpy.ndarray):
            self.hzedgex = hzedgex              # pbc x, TE, custom

        if self.pbcy:
            self.hxedgey = self.hxfield[:,ymax] # pbc y, TM
            self.hzedgey = self.hzfield[:,ymax] # pbc y, TE
        if isinstance(hxedgey, numpy.ndarray):
            self.hxedgey = hxedgey              # pbc y, TM, custom
        if isinstance(hzedgey, numpy.ndarray):
            self.hzedgey = hzedgey              # pbc y, TE, custom
        return self


class UPMLPlane(PlaneDecorator):
    def __init__(self, orig):
        super(UPMLPlane, self).__init__(orig)

        self.pml_thick = 5

        self.pmlx = True
        self.pmly = True

        self.idx = numpy.zeros(self.shape)
        self.idy = numpy.zeros(self.shape)
        self.ibx = numpy.zeros(self.shape)
        self.iby = numpy.zeros(self.shape)

        self.i1 = numpy.zeros(self.shape)
        self.j1 = numpy.zeros(self.shape)

        self.i2 = numpy.ones(self.shape)
        self.j2 = numpy.ones(self.shape)

        self.i3 = numpy.ones(self.shape)
        self.j3 = numpy.ones(self.shape)

        return None

    def pml(self, x=True, y=True, thick=5):
        self.reset_pml()
        self.pmlx = x
        self.pmly = y
        self.pml_thick = thick
        self.set_pml()
        return self

    def update_dfield(self):
        """
        """
        self.idx += self.curl_hx()
        self.idy += self.curl_hy()
        self.dxfield = self.j3 * self.dxfield + self.j2 * 0.5 * ( self.curl_hx() + self.i1 * self.idx )
        self.dyfield = self.i3 * self.dyfield + self.i2 * 0.5 * ( self.curl_hy() + self.j1 * self.idy )
        self.dzfield = self.i3 * self.j3 * self.dzfield + self.i2 * self.j2 * 0.5 * self.curl_hz()
        return self

    def update_bfield(self):
        """
        """
        self.ibx += self.curl_ex()
        self.iby += self.curl_ey()
        self.bxfield = self.j3 * self.bxfield - self.j2 * 0.5 * ( self.curl_ex() + self.i1 * self.ibx )
        self.byfield = self.i3 * self.byfield - self.i2 * 0.5 * ( self.curl_ey() + self.j1 * self.iby )
        self.bzfield = self.i3 * self.j3 * self.bzfield - self.i2 * self.j2 * 0.5 * self.curl_ez()
        return self

    def set_pml(self):
        """
        """
        if self.pmlx:
            for i in range(0, self.pml_thick):
                xn = 0.33 * numpy.power((self.pml_thick - i)/float(self.pml_thick), 3)
                self.i1[i,:] = self.i1[-1-i,:] = xn
                self.i2[i,:] = self.i2[-1-i,:] = 1.0 / ( 1.0 + xn )
                self.i3[i,:] = self.i3[-1-i,:] = ( 1.0 - xn ) / ( 1.0 + xn )
        if self.pmly:
            for j in range(0, self.pml_thick):
                xn = 0.33 * numpy.power((self.pml_thick - j)/float(self.pml_thick), 3)
                self.j1[:,j] = self.j1[:,-1-j] = xn
                self.j2[:,j] = self.j2[:,-1-j] = 1.0 / ( 1.0 + xn )
                self.j3[:,j] = self.j3[:,-1-j] = ( 1.0 - xn ) / ( 1.0 + xn )
        return self

    def reset_pml(self):
        """
        """
        self.i1.fill(0.0)
        self.j1.fill(0.0)
        self.i2.fill(1.0)
        self.j2.fill(1.0)
        self.i3.fill(1.0)
        self.j3.fill(1.0)
        return self

class YTFSFPlane(PlaneDecorator):
    def __init__(self, orig):
        super(YTFSFPlane, self).__init__(orig)
        self.tminc = String(self.shape[1])
        self.teinc = String(self.shape[1])
        self.xtfsf = [10, self.shape[0]-10]
        self.ytfsf = [10, self.shape[1]-10]
        return None
    def update_dtfsf(self):
        if self.xtfsf == [None, None]:
            self.dzfield[:, self.ytfsf[0]]  += 0.5 * self.tminc.hfield[self.ytfsf[0]-1]
            self.dzfield[:, self.ytfsf[1]]  -= 0.5 * self.tminc.hfield[self.ytfsf[1]]
            self.dxfield[:, self.ytfsf[0]]  -= 0.5 * self.teinc.hfield[self.ytfsf[0]-1]
            self.dxfield[:, self.ytfsf[1]]  += 0.5 * self.teinc.hfield[self.ytfsf[1]]
        else:
            # y edge
            self.dzfield[self.xtfsf[0]:self.xtfsf[1]+1, self.ytfsf[0]]  += 0.5 * self.tminc.hfield[self.ytfsf[0]-1]
            self.dzfield[self.xtfsf[0]:self.xtfsf[1]+1, self.ytfsf[1]]  -= 0.5 * self.tminc.hfield[self.ytfsf[1]]
            self.dxfield[self.xtfsf[0]:self.xtfsf[1]+1, self.ytfsf[0]]  -= 0.5 * self.teinc.hfield[self.ytfsf[0]-1]
            self.dxfield[self.xtfsf[0]:self.xtfsf[1]+1, self.ytfsf[1]]  += 0.5 * self.teinc.hfield[self.ytfsf[1]]
            # x edge
            self.dyfield[self.xtfsf[0],   self.ytfsf[0]:self.ytfsf[1]+1] += 0.5 * self.teinc.hfield[self.ytfsf[0]:self.ytfsf[1]+1]
            self.dyfield[self.xtfsf[1]+1, self.ytfsf[0]:self.ytfsf[1]+1] -= 0.5 * self.teinc.hfield[self.ytfsf[0]:self.ytfsf[1]+1]
        return self
    def update_btfsf(self):
        if self.xtfsf == [None, None]:
            # y edge
            self.bxfield[:, self.ytfsf[0]-1]+= 0.5 * self.tminc.efield[self.ytfsf[0]]
            self.bxfield[:, self.ytfsf[1]]  -= 0.5 * self.tminc.efield[self.ytfsf[1]]
            self.bzfield[:, self.ytfsf[0]-1]+= 0.5 * self.teinc.efield[self.ytfsf[0]]
            self.bzfield[:, self.ytfsf[1]]  -= 0.5 * self.teinc.efield[self.ytfsf[1]]
        else:
            # y edge
            self.bxfield[self.xtfsf[0]:self.xtfsf[1]+1, self.ytfsf[0]-1] += 0.5 * self.tminc.efield[self.ytfsf[0]]
            self.bxfield[self.xtfsf[0]:self.xtfsf[1]+1, self.ytfsf[1]]   -= 0.5 * self.tminc.efield[self.ytfsf[1]]
            self.bzfield[self.xtfsf[0]:self.xtfsf[1]+1, self.ytfsf[0]-1] += 0.5 * self.teinc.efield[self.ytfsf[0]]
            self.bzfield[self.xtfsf[0]:self.xtfsf[1]+1, self.ytfsf[1]]   -= 0.5 * self.teinc.efield[self.ytfsf[1]]
            # x edge
            self.byfield[self.xtfsf[0]-1, self.ytfsf[0]:self.ytfsf[1]+1] -= 0.5 * self.tminc.efield[self.ytfsf[0]:self.ytfsf[1]+1]
            self.byfield[self.xtfsf[1],   self.ytfsf[0]:self.ytfsf[1]+1] += 0.5 * self.tminc.efield[self.ytfsf[0]:self.ytfsf[1]+1]
        return self

class XTFSFPlane(PlaneDecorator):
    def __init__(self, orig):
        super(XTFSFPlane, self).__init__(orig)
        self.teinc = String(self.shape[0])
        self.xtfsf = [10, self.shape[0]-10]
        self.ytfsf = [10, self.shape[1]-10]
        return None
    def tfsf(self, xtfsf=None, ytfsf=None, enter = 2):
        self.teinc.enter = enter
        if xtfsf:
            self.xtfsf = xtfsf
        if ytfsf:
            self.ytfsf = ytfsf
        return self
    def update_dtfsf(self):
        if self.ytfsf == [None, None]:
            self.dyfield[self.xtfsf[0],:] += 0.5 * self.teinc.hfield[self.xtfsf[0]-1]
            self.dyfield[self.xtfsf[1],:] -= 0.5 * self.teinc.hfield[self.xtfsf[1]]
        else:
            # x edge
            self.dyfield[self.xtfsf[0],self.ytfsf[0]:self.ytfsf[1]+1] += 0.5 * self.teinc.hfield[self.xtfsf[0]-1]
            self.dyfield[self.xtfsf[1],self.ytfsf[0]:self.ytfsf[1]+1] -= 0.5 * self.teinc.hfield[self.xtfsf[1]]
            # y edge
            self.dxfield[self.xtfsf[0]:self.xtfsf[1],self.ytfsf[0]] -= 0.5 * self.teinc.hfield[self.xtfsf[0]:self.xtfsf[1]]
            self.dxfield[self.xtfsf[0]:self.xtfsf[1],self.ytfsf[1]+1] += 0.5 * self.teinc.hfield[self.xtfsf[0]:self.xtfsf[1]]
        return self
    def update_btfsf(self):
        if self.ytfsf == [None, None]:
            self.bzfield[self.xtfsf[0]-1,:] += 0.5 * self.teinc.efield[self.xtfsf[0]]
            self.bzfield[self.xtfsf[1],:]   -= 0.5 * self.teinc.efield[self.xtfsf[1]]
        else:
            self.bzfield[self.xtfsf[0]-1,self.ytfsf[0]:self.ytfsf[1]+1] += 0.5 * self.teinc.efield[self.xtfsf[0]]
            self.bzfield[self.xtfsf[1],  self.ytfsf[0]:self.ytfsf[1]+1] -= 0.5 * self.teinc.efield[self.xtfsf[1]]
        return self

class DispersivePlane(PlaneDecorator):
    def __init__(self, orig):
        super(DispersivePlane, self).__init__(orig)
        self.epsilon_rx = numpy.ones(self.shape)
        self.epsilon_ry = numpy.ones(self.shape)
        self.epsilon_rz = numpy.ones(self.shape)
        self.mu_rx      = numpy.ones(self.shape)
        self.mu_ry      = numpy.ones(self.shape)
        self.mu_rz      = numpy.ones(self.shape)
        return None
    def update_efield(self, *polar):
        self.exfield  = self.dxfield.copy()
        self.eyfield  = self.dyfield.copy()
        self.ezfield  = self.dzfield.copy()
        for p in polar:
            self.exfield -= p.x
            self.eyfield -= p.y
            self.ezfield -= p.z
        self.exfield /= self.epsilon_rx
        self.eyfield /= self.epsilon_ry
        self.ezfield /= self.epsilon_rz
        return self
    def update_hfield(self, *polar):
        self.hxfield  = self.bxfield.copy()
        self.hyfield  = self.byfield.copy()
        self.hzfield  = self.bzfield.copy()
        for p in polar:
            self.hxfield -= p.x # should verify + or -
            self.hyfield -= p.y
            self.hzfield -= p.z
        self.hxfield /= self.mu_rx
        self.hyfield /= self.mu_ry
        self.hzfield /= self.mu_rz
        return self
    def circle_e(self, center, r, value):
        circle(self.epsilon_rx, twodim.center_ex(center), r, value)
        circle(self.epsilon_ry, twodim.center_ey(center), r, value)
        circle(self.epsilon_rz, twodim.center_ez(center), r, value)
        return self

    def circle_m(self, center, r, value):
        # not yet implement
        return self

    def rectangle_e(self, center, xlen, ylen, value):
        rectangle(self.epsilon_rx, twodim.center_ex(center), xlen, ylen, value)
        rectangle(self.epsilon_ry, twodim.center_ey(center), xlen, ylen, value)
        rectangle(self.epsilon_rz, twodim.center_ez(center), xlen, ylen, value)
        return self

    def rectangle_m(self, center, xlen, ylen, value):
        # not yet implement
        return self

class PolarDPlane(object):
    def __init__(self, shape, a=0, b=0, c=1, d=0, dt=1):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.dt = dt
        self.maskx=numpy.zeros(shape)
        self.masky=numpy.zeros(shape)
        self.maskz=numpy.zeros(shape)
        self.x   = numpy.zeros(shape)
        self.y   = numpy.zeros(shape)
        self.z   = numpy.zeros(shape)
        self.xp  = numpy.zeros(shape)
        self.yp  = numpy.zeros(shape)
        self.zp  = numpy.zeros(shape)
        self.xp2 = numpy.zeros(shape)
        self.yp2 = numpy.zeros(shape)
        self.zp2 = numpy.zeros(shape)
        return None

    def update(self, plane):
        self.xp2 = self.xp
        self.yp2 = self.yp
        self.zp2 = self.zp
        self.xp = self.x
        self.yp = self.y
        self.zp = self.z
        self.x = self.c1*self.xp + self.c2*self.xp2 + self.c3*plane.exfield*self.maskx
        self.y = self.c1*self.yp + self.c2*self.yp2 + self.c3*plane.eyfield*self.masky
        self.z = self.c1*self.zp + self.c2*self.zp2 + self.c3*plane.ezfield*self.maskz
        return self

    def set_factor(self):
        denominator = 2*self.d + self.c*self.dt
        self.c1 = (4*self.d - 2*self.b*(self.dt**2)) / denominator
        self.c2 = (-2*self.d + self.c*self.dt) / denominator
        self.c3 = (2*self.a*(self.dt**2)) / denominator
        return self

    def circle(self, center, r):
        circle(self.maskx, twodim.center_ex(center), r, 1)
        circle(self.masky, twodim.center_ey(center), r, 1)
        circle(self.maskz, twodim.center_ez(center), r, 1)
        return self

    def rectangle(self, center, xlen, ylen, value):
        rectangle(self.maskx, twodim.center_ex(center), xlen, ylen, 1)
        rectangle(self.masky, twodim.center_ey(center), xlen, ylen, 1)
        rectangle(self.maskz, twodim.center_ez(center), xlen, ylen, 1)
        return self


class Cube(object):
    """ Three dimension grid object """
    
    def __init__(self, shape):
        """
        Arguments:
        - `shape`: specify plance shape
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

    def update_dfield(self):
        """
        """
        self.dxfield += 0.5 * self.curl_hx()
        self.dyfield += 0.5 * self.curl_hy()
        self.dzfield += 0.5 * self.curl_hz()
        return self

    def update_efield(self):
        """
        """
        self.exfield = self.dxfield.copy()
        self.eyfield = self.dyfield.copy()
        self.ezfield = self.dzfield.copy()
        return self

    def update_bfield(self):
        """
        """
        self.bxfield -= 0.5 * self.curl_ex()
        self.byfield -= 0.5 * self.curl_ey()
        self.bzfield -= 0.5 * self.curl_ez()
        return self

    def update_hfield(self):
        """
        """
        self.hxfield = self.bxfield.copy()
        self.hyfield = self.byfield.copy()
        self.hzfield = self.bzfield.copy()
        return self

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

        
