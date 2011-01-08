import sys
# sys.path += ["/opt/local/Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/site-packages"]

exec "import %s as target" % sys._getframe(1).f_globals["__name__"]

modules = (
    "sys",
    "os",
    "matplotlib",
    "numpy",
    "scipy",
    "timeit",
    "h5py",
)
    
target.__dict__.update( dict(zip(modules, [__import__(m) for m in modules])) )

target.matplotlib.use("Agg")

target.__dict__.update({
    "pylab"   :   __import__("pylab"),                          # this should be eval after setting Agg backend
    "pprint"  :   __import__("pprint").pprint,                  # import function
})

exec "import yafdtd" in target.__dict__                         # another way
