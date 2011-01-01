#!/usr/bin/env python

from multiprocessing import Process
import matplotlib, pylab
from matplotlib import _pylab_helpers, cm

def plot(name):
  fig = pylab.figure()
  ax = fig.gca()
  ax.plot([1,2,3,4])
  fig.savefig("/tmp/"+str(name)+".png")
  _pylab_helpers.Gcf.destroy_fig(fig)

threads = []

for x in range(50):
  threads.append(Process(target=plot,args=(x,)))

for t in threads:
  t.start()

for t in threads:
  t.join()
