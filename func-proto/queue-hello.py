#!/usr/bin/env python

import Queue

queue = Queue.Queue()
queue.put(1)
print queue.get()
print queue.qsize()
try:
  print queue.get_nowait()
except Queue.Empty:
  pass

