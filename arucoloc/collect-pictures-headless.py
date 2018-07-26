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

headless = True

vc = cv2.VideoCapture(0)
i = 0
while True:
    try:
        input("Press Enter to save a picture, Ctrl-C to stop.")
    except SyntaxError:
        pass
    ofn = 'shot-%02i.jpg' % i

    retval, img = vc.read() # Capture frame-by-frame
    eprint("Saving ", ofn)
    cv2.imwrite(ofn, img)
    i += 1
