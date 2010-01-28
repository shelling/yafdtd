
def import_convention(scope):
    code =\
"""
import sys, os, matplotlib, mpmath, numpy
sys.path += ["lib","/opt/local/Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/site-packages"]
matplotlib.use("Agg")
import pylab
import scipy
from pprint import pprint
"""
    exec code in scope
    pass
