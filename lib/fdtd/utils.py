import matplotlib
import pylab
import numpy
import shutil

from matplotlib import cm, _pylab_helpers, interactive
from mpl_toolkits.mplot3d import Axes3D

def save_field(field, filename_pattern, id, intensity=[-1,1]):
    """
    shortcut for saving file through matplotlib
    
    Arguments:
    - `field`: the field 
    - `filename_pattern`: the filename pattern 
    - `id`: the distinguish identity would be applied to filename pattern
    - `intensity`: the range of field intensity show on y-index of plot
    """
    if len(field.shape) == 1:
        pylab.grid(True)
        pylab.plot(field)
        pylab.ylim( intensity )
        pylab.xlim( [0, field.shape[0]-1] )
        pylab.savefig(filename_pattern % id)
        pylab.clf()
        # should be rewritten to use local figure
        
    elif len(field.shape) == 2:
        fig = pylab.figure()
        im = fig.gca().imshow( field, norm=matplotlib.colors.Normalize( *(intensity + [True]) ) )
        fig.colorbar(im)
        fig.savefig(filename_pattern % id)
        # _pylab_helpers.Gcf.destroy_all()
        _pylab_helpers.Gcf.destroy_fig(fig)
        
    elif len(field.shape) == 3:
        pass
    else:
        raise TypeError("save_field takes 1 to 3 dimension(s) numpy.ndarray")
        # shoudld raise dimension error here
        pass
    return None

def save_field_surf(field, filename_pattern, id, intensity=[-1,1]):
    """
    shortcut for saving field as 3D plot through matplotlib

    Arguments:
    -`field`: the field
    -`filename_pattern': the filename pattern
    -`id`: the distinguish identity would be applied to filename pattern
    -`intensity`: the range of field intensity show on z-index of plot
    """
    x = numpy.arange(0,field.shape[0])
    y = numpy.arange(0,field.shape[1])
    x, y = numpy.meshgrid(x, y)
    fig = pylab.figure()
    ax = fig.gca(projection="3d")
    ax.plot_surface(x, y, field, rstride=1, cstride=1, cmap=cm.jet, linewidth=0, antialiased=False, norm=matplotlib.colors.Normalize(-1,1,True))
    ax.set_zlim3d([-1,1])
    fig.savefig(filename_pattern % id)
    # _pylab_helpers.Gcf.destroy_all()
    _pylab_helpers.Gcf.destroy_fig(fig)
    return None

def open(dir):
  """
  open directory in gui file browser is possible
  """
  filebrowser = {"Darwin": "open", "Linux": "nautilus"}
  os.system(filebrowser[os.uname()[0]]+" "+dir)
  return None
