#!/usr/bin/env python2
# From: https://gist.github.com/hauptmech/6b8ca2c05a3d935c97b1c75ec9ad85ff
# Needs to install: sudo pip2 install opencv-contrib-python
# Runs video capture and locates aruco markers from the given dictionary.

# python print to stderr (most portable and flexible)
from __future__ import print_function
import sys
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

import numpy as np
import cv2

cap = cv2.VideoCapture(0)
#dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_1000)
#dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)
#dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL)

i = 0
while True:
    try:
        input("Press Enter to save a picture of hopefully located markers, Ctrl-C to stop.")
    except SyntaxError:
        pass

    eprint("Capturing image")
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    eprint("Grayscale")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    eprint("Detecting")
    res = cv2.aruco.detectMarkers(gray,dictionary)
    found = len(res[0])
    eprint("Found ", found, " markers")
#   print(res[0],res[1],len(res[2]))

    if len(res[0]) > 0:
        eprint("Drawing detected")
        cv2.aruco.drawDetectedMarkers(gray,res[0],res[1])
    # Save the resulting frame
    ofn = 'shot-%02i-found%02i.jpg' % (i, found)
    eprint("Saving")
    cv2.imwrite(ofn, gray)
    i += 1

# When everything done, release the capture
cap.release()
