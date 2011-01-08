#!/usr/bin/env python

import Queue

queue = Queue.Queue()

[queue.put(x) for x in range(30)]

print "size: ", queue.qsize()

while True:
    try:
        print queue.get_nowait()
    except Queue.Empty:
        break

