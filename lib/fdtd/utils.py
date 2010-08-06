import matplotlib
import pylab

def save_field(field, filename_pattern, id, intensity=[-1,1]):
    """
    shortcut for saving file through matplotlib
    
    Arguments:
    - `field`: the field 
    - `filename_pattern`: the filename pattern 
    - `id`: the distinguish identity would be applied to filename pattern
    - `intensity`: the range of field intensity show on plot
    """
    if len(field.shape) == 1:
        pylab.grid(True)
        pylab.plot(field)
        pylab.ylim( intensity )
        
    elif len(field.shape) == 2:
        pylab.imshow( field, norm=matplotlib.colors.Normalize( *(intensity + [True]) ) )
        pylab.colorbar()
        
    elif len(field.shape) == 3:
        pass
    else:
        pass
    
    pylab.savefig(filename_pattern % id)
    pylab.clf()
    
    return None
