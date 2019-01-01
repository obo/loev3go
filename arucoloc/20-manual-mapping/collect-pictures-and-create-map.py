#!/usr/bin/env python
# Run on robot (or notebook)
# Have mapper_from_images (from marker_mapper) in your path
# It will take a picture at every return key
# It will try to build a map at every X collects.

# python print to stderr (most portable and flexible)
from __future__ import print_function
import sys
verbose = False
def eprint(*args, **kwargs):
    if verbose: print(*args, file=sys.stderr, **kwargs)

import datetime
import numpy as np
import cv2
import os
import re

calibration_file = "calibration.yaml"
dictfile = "DICT_6x6_250.dict"
map_every = 3 # try marker_mapper every 5 saved pictures

# create timestamped directory
d = datetime.datetime.now() 
ts = '%04d%02d%02d-%02d%02d%02d' % (d.year, d.month, d.day, d.hour, d.minute, d.second)
dirname = "shots-"+ts
os.mkdir(dirname)

# prepare image capturing
vc = cv2.VideoCapture(0)

# prepare detection of aruco markers
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_6X6_250)

def run_marker_mapper(dirname):
  ret = os.system("mapper_from_images %s %s 0.04 %s %s/map" % (dirname, calibration_file, dictfile, dirname))
  if ret == 0:
    eprint("mapper_from_images claims to have SUCCEEDED")
  else:
    eprint("mapper_from_images seems FAILED")
  mapfile = '%s/map.yml' % dirname
  if os.path.isfile(mapfile):
    eprint("Testing and fixing the mapfile")
    with open(mapfile) as inf:
      text = inf.read();
    # extract the number of markers
    num_markers_re = re.compile(r"aruco_bc_nmarkers: *([0-9])")
    num_markers = num_markers_re.search(text)
    if num_markers:
      eprint("GOT THIS MANY MARKERS: ", num_markers.group(1))
      if num_markers > 0:
        # replace the bad filename
        dictfn_re = re.compile(r"aruco_bc_dict: [^ \n]*")
        text = dictfn_re.sub(r'aruco_bc_dict: "../DICT_6x6_250.dict"', text)
        # save the corrected map:
        with open(mapfile, 'w') as outf:
          outf.write(text);
        return True
  else:
    return False

def find_my_position(calibration_file, map_file, image_file):
  ret = os.system("aruco_locate_one %s %s %s" % (image_file, map_file, calibration_file))
  if ret == 0:
    eprint("aruco_locate_one claims to have SUCCEEDED")
  else:
    eprint("aruco_locate_one seems FAILED")

i = 0
have_map = False # we don't have any map at hand yet
while True:
    try:
        input("Targetdir: "+dirname+". Press Enter for a picture, Ctrl-C to stop.")
    except SyntaxError:
        pass
    # Capture one frame
    eprint("Smile, taking one picture.")
    retval, img = vc.read()
    # Check if it contains markers
    eprint("Checking if it contains markers.")
    res = cv2.aruco.detectMarkers(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY),
                                  dictionary)
    found = len(res[0])
    if (found > 1):
      ofn = '%s/shot-%02i.jpg' % (dirname, i)
      eprint("Saving ", ofn, ", it contained ", found, " markers.")
      cv2.imwrite(ofn, img)
      i += 1
      # if we already have a map, find our position
      if have_map:
        find_my_position(calibration_file, dirname+"/map.yml", ofn)
      # run marker mapper every now and then, to improve the map
      if (i % map_every == 0) :
        have_map = run_marker_mapper(dirname)
    else:
      eprint("Not saving, only ", found, " markers.")
    # fi
vc.release()

if (i % map_every != 0):
  # run marker mapper, it was not run before
  run_marker_mapper(dirname)
