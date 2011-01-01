#!/usr/bin/env python

import threading, Queue

Pool = Queue.Queue()
for x in xrange(0,1000000):
  Pool.put(x)

def plot():
  while 1:
    try:
      print Pool.get(False)
    except Queue.Empty:
      break


threads = []
for x in range(8):
  threads.append(threading.Thread(target=plot))

for t in threads:
  t.start()

for t in threads:
  t.join()
