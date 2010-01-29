import sys
sys.path += ["lib","/opt/local/Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/site-packages"]

caller = sys._getframe(1).f_globals["__name__"]
exec "import %s as target" % caller

target.timeit = __import__("timeit")

modules = (
    "sys",
    "os",
    "matplotlib",
    "mpmath",
    "numpy",
    "scipy",
    "timeit"
)
    
for module_name in modules:
    target.__dict__[module_name] = __import__(module_name)

target.matplotlib.use("Agg")
target.mpmath.mp.dps = 100

target.__dict__["pylab"] = __import__("pylab")
target.__dict__["pprint"] = __import__("pprint").pprint


# below is obsolete
# {{{

def import_convention(scope):
    code =\
"""
import sys, os, matplotlib, mpmath, numpy
sys.path += ["lib","/opt/local/Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/site-packages"]
mpmath.mp.dps = 100
matplotlib.use("Agg")
import pylab
import scipy
from pprint import pprint
import fdtd
"""
    exec code in scope
    pass

# }}}
