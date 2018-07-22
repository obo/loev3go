#!/usr/bin/env python
# Grab one picture

# python print to stderr (most portable and flexible)
from __future__ import print_function
import sys
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

import numpy as np
import cv2
import yaml

vc = cv2.VideoCapture(1)
k = -1 & 0xff
i = 0
while k != 27:
    retval, img = vc.read() # Capture frame-by-frame
    cv2.imshow('img', img)
    k = cv2.waitKey(100)
    eprint(k)
    if k == 10 or k == 13:
      ofn = 'shot-%02i.jpg' % i
      eprint("Saving ", ofn)
      cv2.imwrite(ofn, img)
      i += 1
