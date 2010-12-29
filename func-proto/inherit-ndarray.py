#!/usr/bin/env python
#-*- mode: python -*-

import numpy

class Plane(numpy.ndarray):
    """
    
    """
    def __new__(cls, abuffer):
        """
        create a new plane object
        """
        abuffer = numpy.array(abuffer, dtype="float128")
        if len(abuffer.shape) == 2:
            return numpy.ndarray.__new__(cls, abuffer.shape, "float128", abuffer)
        else:
            pass

    def __array_finalize__(self, obj):
        pass
            
    @property
    def name(self, name):
        self.name = name
        return self
    

p = Plane([[1,2,],[3,4]])
print p
print p.shape
print p.dtype
print p.__class__
