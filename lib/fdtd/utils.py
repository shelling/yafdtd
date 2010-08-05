import pylab

def save_field(field, filename_pattern, id, axis=None):
    """
    shortcut for saving file through matplotlib
    
    Arguments:
    - `field`:
    - `filename_pattern`:
    - `id`:
    - `axis`:
    """
    pylab.grid(True)
    pylab.plot(field)
    pylab.ylim([-1,1])
    pylab.savefig(filename_pattern % id)
    pylab.clf()
    return None
