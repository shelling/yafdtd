"""
Unaxial Perfect Matched Layer (UPML) related functions
"""

from __future__ import division         # using real division with / operator

import mpmath
import math
import numpy
import pylab



def update_efield( plane, region=None ):
    """
    2-D field update equation upon Unaxial PML
    using region to specify work region, or work on whole region
    
    Arguments:
    - `plane`: fdtd.grid.Plane instance
    - `region`: the region would be updated
    """
    
    (xaxis, yaxis) = plane.shape
    
    if plane.transverse == "TE":
        pass
    elif plane.transverse == "TM":
        for i in range(1,xaxis-1):
            for j in range(1,yaxis-1):
                plane.ezfield[i,j] = plane.gi3[i] * plane.gj3[j] * plane.ezfield[i,j] + plane.gi2[i] * plane.gj2[j] * 0.5 * ( plane.hyfield[i,j] - plane.hyfield[i-1,j] - plane.hxfield[i,j] + plane.hxfield[i,j-1] )
                # plane.ezfield[i,j] = plane.gi3[i] * plane.gj3[j] * plane.ezfield[i,j] + plane.gi2[i] + plane.gj2[j] * 0.5 * ( plane.hyfield[i,j] - plane.hyfield[i-1,j] - plane.hxfield[i,j] + plane.hxfield[i,j-1] )
    
    return None

def update_hfield( plane, region=None ):
    """
    2-D field update equation upon Unaxial PML
    using region to specify work region, or work on whole region
    
    Arguments:
    - `plane`:
    - `region`:
    """
    (xaxis,yaxis) = plane.shape

    if plane.transverse == "TE":
        pass
    elif plane.transverse == "TM":
        for i in xrange(0,xaxis-1):
            for j in xrange(0,yaxis-1):
                curl_e = plane.ezfield[i,j] - plane.ezfield[i,j+1]
                plane.ihx[i,j] = plane.ihx[i,j] + curl_e
                plane.hxfield[i,j] = plane.fj3[j] * plane.hxfield[i,j] + plane.fj2[j] * 0.5 * curl_e + plane.fi1[i] * plane.ihx[i,j]

                curl_e = plane.ezfield[i+1,j] - plane.ezfield[i,j]
                plane.ihy[i,j] = plane.ihy[i,j] + curl_e                
                plane.hyfield[i,j] = plane.fi3[i] * plane.hyfield[i,j] + plane.fi2[i] * 0.5 * curl_e + plane.fj1[j] * plane.ihy[i,j]
    return None



def append_pml( plane, thick=8 ):
    """
    append perfect matched layer and related parameters to surround of problem region

    parameters of PML itself:
    gi2, gi3, fi1, fi2, fi3
    gj2, gj3, fj1, fj2, fj3

    other parameters:
    ihx, ihy
    
    Arguments:
    - `plane`: fdtd.grid.Plane instance
    - `thick`: the number of cells PML would occupy
    """
    if plane.shape[0] < thick * 2 or plane.shape[1] < thick * 2:
        # raise error here
        pass
    # append parameters for BPML
    plane.pml_thick = thick

    (x,y) = plane.shape
    
    plane.ihx = numpy.zeros(plane.shape)
    plane.ihy = numpy.zeros(plane.shape)

    plane.gi2 = numpy.ones(x)
    plane.gi3 = numpy.ones(x)

    plane.gj2 = numpy.ones(y)
    plane.gj3 = numpy.ones(y)

    plane.fi1 = numpy.zeros(x)
    plane.fi2 = numpy.ones(x)
    plane.fi3 = numpy.ones(x)

    plane.fj1 = numpy.zeros(y)
    plane.fj2 = numpy.ones(y)
    plane.fj3 = numpy.ones(y)

    # calculate PML parameters
    for i in range(0, int(thick) ):
        xn = 0.33 * math.pow( (thick - i)/thick, 3.0 )
        plane.gi2[i] = plane.gi2[-1-i] = 1.0 / (1.0 + xn)
        plane.gi3[i] = plane.gi3[-1-i] = (1.0 - xn) / (1.0 + xn)
        plane.fi1[i] = plane.fi1[-1-i] = xn
        plane.fi2[i] = plane.fi2[-1-i] = 1.0 / (1.0 + xn)
        plane.fi3[i] = plane.fi3[-1-i] = (1.0 - xn) / (1.0 + xn)
        
    for j in range(0, int(thick) ):
        xn = 0.33 * math.pow( (thick -j)/thick, 3.0 )
        plane.gj2[j] = plane.gj2[-1-j] = 1.0 / (1.0 + xn)
        plane.gj3[j] = plane.gj3[-1-j] = (1.0 - xn) / (1.0 + xn)
        plane.fj1[j] = plane.fj1[-1-j] = xn
        plane.fj2[j] = plane.fj2[-1-j] = 1.0 / (1.0 + xn)
        plane.fj3[j] = plane.fj3[-1-j] = (1.0 - xn) / (1.0 + xn)
    return None


def strip_pml(plane):
    """
    strip UPML from plane instance
    
    Arguments:
    - `plane`:
    """
    return None


def plot_pml_params(plane, filename):
    """
    
    
    Arguments:
    - `plane`:
    - `filename`:
    """
    pylab.subplot(211)
    for item in [plane.gi2, plane.gi3, plane.fi1, plane.fi2, plane.fi3]:
        pylab.plot(item)
    pylab.grid(True)
    pylab.subplot(212)
    for item in [plane.gj2, plane.gj3, plane.fj1, plane.fj2, plane.fj3]:
        pylab.plot(item)
    pylab.grid(True)
    pylab.savefig(filename)
    pylab.clf()
    return None



class UPML(object):
    """
    Unaxial Perfect Matched Layer object, storing g and f parameters for update equations
    """
    
    def __init__(self, plane, thick=8.0):
        """

        Arguments:
        -`plane`:
        -`thick`:
        """
        self.thick = thick
        
        (x, y) = plane.shape

        self.gi2 = numpy.ones(x)
        self.gi3 = numpy.ones(x)
        
        self.gj2 = numpy.ones(y)
        self.gj3 = numpy.ones(y)

        self.fi1 = numpy.zeros(x)
        self.fi2 = numpy.ones(x)
        self.fi3 = numpy.ones(x)

        self.fj1 = numpy.zeros(y)
        self.fj2 = numpy.ones(y)
        self.fj3 = numpy.ones(y)

        self.enable()

        return None


    def enable(self):
        """
        calculate g and f parameters of UPML itself
        
        Arguments:
        - `self`:
        """
        thick = self.thick
        
        for i in range(0, int(thick) ):
            xn = 0.33 * math.pow( (thick - i)/thick, 3 )
            self.gi2[i] = self.gi2[-1-i] = 1.0 / (1.0 + xn)
            self.gi3[i] = self.gi3[-1-i] = (1.0 - xn) / (1.0 + xn)
            self.fi1[i] = self.fi1[-1-i] = xn
            self.fi2[i] = self.fi2[-1-i] = 1.0 / (1.0 + xn)
            self.fi3[i] = self.fi3[-1-i] = (1.0 - xn) / (1.0 + xn)
        
        for j in range(0, int(thick) ):
            xn = 0.33 * math.pow( (thick -j)/thick, 3.0 )
            self.gj2[j] = self.gj2[-1-j] = 1.0 / (1.0 + xn)
            self.gj3[j] = self.gj3[-1-j] = (1.0 - xn) / (1.0 + xn)
            self.fj1[j] = self.fj1[-1-j] = xn
            self.fj2[j] = self.fj2[-1-j] = 1.0 / (1.0 + xn)
            self.fj3[j] = self.fj3[-1-j] = (1.0 - xn) / (1.0 + xn)

        return self

    def disable(self):
        """
        set g2, g3, f2, f3 to one, f1 to zero to disable UPML
        
        """
        for item in [
            self.gi2,
            self.gi3,
            self.fi2,
            self.fi3,
            self.gj2,
            self.gj3,
            self.fj2,
            self.fj3]:
            item.fill(1)
            
        for item in [
            self.fi1,
            self.fj1]:
            item.fill(0)
        
        return self

    def plot(self, filename):
        """
        plot g and f parameters of PML itself
        
        Arguments:
        - `filename`:
        """
        pylab.subplot(211)
        for item in [self.gi2, self.gi3, self.fi1, self.fi2, self.fi3]:
            pylab.plot(item)
        pylab.grid(True)
        pylab.subplot(212)
        for item in [self.gj2, self.gj3, self.fj1, self.fj2, self.fj3]:
            pylab.plot(item)
        pylab.grid(True)
        pylab.savefig(filename)
        pylab.clf()
        return None


        
