"""
Unaxial Perfect Matched Layer (UPML) related functions
"""

from __future__ import division         # using real division with / operator

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
    
    (x, y) = plane.shape
    pml    = plane.pml
    
    if plane.transverse == "TE":
        pass
    elif plane.transverse == "TM":
        for i in range(1,x-1):
            for j in range(1,y-1):
                plane.dzfield[i,j] = pml.gi3[i] * pml.gj3[j] * plane.dzfield[i,j] + pml.gi2[i] * pml.gj2[j] * 0.5 * ( plane.hyfield[i,j] - plane.hyfield[i-1,j] - plane.hxfield[i,j] + plane.hxfield[i,j-1] )
                plane.ezfield[i,j] = plane.ga[i,j] * plane.dzfield[i,j]
    return None

def update_dfield(self, region=None ):
    """
    
    Arguments:
    - `region`:
    """
    return None


def update_hfield( plane, region=None ):
    """
    2-D field update equation upon Unaxial PML
    using region to specify work region, or work on whole region
    
    Arguments:
    - `plane`:
    - `region`:
    """
    (x, y) = plane.shape
    pml    = plane.pml

    if plane.transverse == "TE":
        pass
    elif plane.transverse == "TM":
        for i in xrange(0,x-1):
            for j in xrange(0,y-1):
                curl_e = plane.ezfield[i,j] - plane.ezfield[i,j+1]
                plane.ihx[i,j] = plane.ihx[i,j] + curl_e
                plane.hxfield[i,j] = pml.fj3[j] * plane.hxfield[i,j] + pml.fj2[j] * 0.5 * curl_e + pml.fi1[i] * plane.ihx[i,j]

                curl_e = plane.ezfield[i+1,j] - plane.ezfield[i,j]
                plane.ihy[i,j] = plane.ihy[i,j] + curl_e                
                plane.hyfield[i,j] = pml.fi3[i] * plane.hyfield[i,j] + pml.fi2[i] * 0.5 * curl_e + pml.fj1[j] * plane.ihy[i,j]
    return None

def update_bfield(self, region=None):
    """
    
    Arguments:
    - `region`:
    """
    return None



class UPML(object):
    """
    Unaxial Perfect Matched Layer object, storing g and f parameters for update equations
    """
    
    def __init__(self, shape, thick=8):
        """

        Arguments:
        -`plane`:
        -`thick`:
        """
        self.thick = thick
        self.shape = shape
        
        (x, y) = shape

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

    def stick(self, plane):
        """
        append the UPML instance to a Plane instance
        
        Arguments:
        - `plane`: the Plane instance would append the UPML instance
        """
        self.host = plane
        plane.pml = self
        return None

    def strip(self, ):
        """
        strip the UPML instance itself from a Plane instance
        """
        self.host.pml = None
        self.host = None
        return None

