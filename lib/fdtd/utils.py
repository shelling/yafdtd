import matplotlib
import pylab
import numpy
import os
import shutil

from matplotlib import cm, _pylab_helpers, interactive
from mpl_toolkits.mplot3d import Axes3D

def fft(t, timedomain, sampleperiod):
    n = len(t)
    f = numpy.arange(-n/2,n/2)/(sampleperiod*n)
    freqdomain = numpy.abs(numpy.fft.fftshift(numpy.fft.fft(timedomain)))
    return f, freqdomain

def plot(field, pattern, id, range=[-1,1]):
    fig = pylab.figure()
    ax = fig.gca()
    ax.plot(field)
    ax.set_ylim(range)
    ax.set_xlim(0,field.shape[0]-1)
    fig.savefig(pattern % id)
    _pylab_helpers.Gcf.destroy_fig(fig)
    return None

def imshow(field, pattern, id, intensity=[-1,1]):
    fig = pylab.figure()
    im = fig.gca().imshow( field, norm=matplotlib.colors.Normalize( *(intensity + [True]) ) )
    fig.colorbar(im)
    fig.savefig(pattern % id)
    _pylab_helpers.Gcf.destroy_fig(fig)
    return None

def surf(field, pattern, id, intensity=[-1,1]):
    """
    shortcut for saving field as 3D plot through matplotlib

    Arguments:
    -`field`: the field
    -`pattern': the filename pattern
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
    fig.savefig(pattern % id)
    _pylab_helpers.Gcf.destroy_fig(fig)
    return None

def split(alist, length):
    result = []
    head = 0
    while head < len(alist):
      result.append(alist[head:head+length])
      head += length
    return result

filebrowser = {"Darwin": "open", "Linux": "nautilus"}
def open(dir):
    """
    open directory in gui file browser is possible
    """
    app = filebrowser[os.uname()[0]]
    os.system(app+" "+dir) if app else None
    return None
