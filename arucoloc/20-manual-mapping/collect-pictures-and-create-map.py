#!/usr/bin/env python
# Run on robot (or notebook)
# Have mapper_from_images (from marker_mapper) in your path
# It will take a picture at every return key
# It will try to build a map at every X collects.

# python print to stderr (most portable and flexible)
from __future__ import print_function
import sys
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

import datetime
import numpy as np
import cv2
import yaml
import os

# create timestamped directory
d = datetime.datetime.now() 
ts = '%04d%02d%02d-%02d%02d%02d' % (d.year, d.month, d.day, d.hour, d.minute,
d.second)
dirname = "shots-"+ts
os.mkdir(dirname)

vc = cv2.VideoCapture(0)
i = 0
while True:
    try:
        input("Saving pictures to "+dirname+". Press Enter for a picture, Ctrl-C to stop.")
    except SyntaxError:
        pass
    ofn = '%s/shot-%02i.jpg' % (dirname, i)

    retval, img = vc.read() # Capture frame-by-frame
    eprint("Saving ", ofn)
    cv2.imwrite(ofn, img)
    i += 1
vc.release()
