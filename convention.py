import sys
sys.path += ["/opt/local/Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/site-packages"]

caller = sys._getframe(1).f_globals["__name__"]
exec "import %s as target" % caller

modules = (
    "sys",
    "os",
    "matplotlib",
    "numpy",
    "scipy",
    "timeit"
)
    
for module_name in modules:
    target.__dict__[module_name] = __import__(module_name)

target.matplotlib.use("Agg")

target.__dict__["pylab"] = __import__("pylab")                # this should be eval after setting Agg backend
target.__dict__["pprint"] = __import__("pprint").pprint       # import function




# below is obsolete
# {{{

def import_convention(scope):
    code =\
"""
import sys, os, matplotlib, numpy
sys.path += ["/opt/local/Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/site-packages"]
matplotlib.use("Agg")
import pylab
import scipy
from pprint import pprint
import yafdtd
"""
    exec code in scope
    pass

# }}}
