"""
Berenger's Perfect Matched Layer (BPML) related functions
"""

import mpmath
import math
import numpy
import pylab

def update_efield( plane, region=None ):
    """
    2-D E field update eqution upon Berenger's PML
    using region to specify work region, or work on whole region
    
    Arguments:
    - `plane`: fdtd.grid.Plane instance
    - `region`: the region would be updated
    """

    (xaxis,yaxis) = plane.shape

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
    2-D H field update equation upon Berenger's PML
    using region to specify work region, or work on whole region
    
    Arguments:
    - `plane`: fdtd.grid.Plane instance
    - `region`: the region would be updated
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

def append_pml( plane, thick=8.0 ):
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

    shape = plane.shape
    
    plane.ihx = numpy.zeros(shape)
    plane.ihy = numpy.zeros(shape)

    plane.gi2 = numpy.ones(shape[0])
    plane.gi3 = numpy.ones(shape[0])

    plane.gj2 = numpy.ones(shape[1])
    plane.gj3 = numpy.ones(shape[1])

    plane.fi1 = numpy.zeros(shape[0])
    plane.fi2 = numpy.ones(shape[0])
    plane.fi3 = numpy.ones(shape[0])

    plane.fj1 = numpy.zeros(shape[1])
    plane.fj2 = numpy.ones(shape[1])
    plane.fj3 = numpy.ones(shape[1])

    # calculate PML parameters
    for i in range(0, int(thick) ):
        xn = 0.33 * math.pow( (thick - i)/thick, 3.0 )
        plane.gi2[i] = plane.gi2[plane.shape[0]-1-i] = 1.0 / (1.0 + xn)
        plane.gi3[i] = plane.gi3[plane.shape[0]-1-i] = (1.0 - xn) / (1.0 + xn)
        
        #xn = 0.25 * math.pow( (thick - i - 0.5) / thick, 3.0 )
        plane.fi1[i] = plane.fi1[plane.shape[1]-1-i] = xn
        plane.fi2[i] = plane.fi2[plane.shape[1]-1-i] = 1.0 / (1.0 + xn)
        plane.fi3[i] = plane.fi3[plane.shape[1]-1-i] = (1.0 - xn) / (1.0 + xn)
        
    for j in range(0, int(thick) ):
        xn = 0.33 * math.pow( (thick -j)/thick, 3.0 )
        plane.gj2[j] = plane.gj2[plane.shape[1]-1-j] = 1.0 / (1.0 + xn)
        plane.gj3[j] = plane.gj3[plane.shape[1]-1-j] = (1.0 - xn) / (1.0 + xn)

        #xn = 0.25 * math.pow( (thick - j - 0.5 ) / thick, 3.0 )
        plane.fj1[j] = plane.fj1[plane.shape[1]-1-j] = xn
        plane.fj2[j] = plane.fj2[plane.shape[1]-1-j] = 1.0 / (1.0 + xn)
        plane.fj3[j] = plane.fj3[plane.shape[1]-1-j] = (1.0 - xn) / (1.0 + xn)
    return None

def strip_pml(plane):
    """
    stripe BPML from problem region
    
    Arguments:
    - `plane`:
    """
    for item in [plane.gi2, plane.gi3, plane.fi2, plane.fi3, plane.gj2, plane.gj3, plane.fj2, plane.fj3 ]:
        item.fill(1.0)
    for item in [plane.fi1, plane.fj1]:
        item.fill(0.0)
    return None

class BPML(object):
    """
    Berenger's PML object, storing g and f parameters for update equations
    """
    
    def __init__(self, thick):
        """
        
        Arguments:
        - `thick`:
        """
        self.thick = thick
        return None
    

    def enable(self):
        """
        enable myself
        """
        return self


    def disable(self, ):
        """
        disable myself
        """
        return self


    def plot(self, filename):
        """
        plot parameters of Berenger's PML

        Arguments:
        - `filename`:
        """
        return None
