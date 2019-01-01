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
import subprocess

calibration_file = "calibration.yaml"
dictfile = "DICT_6x6_250.dict"
map_every = 3 # try marker_mapper every 5 saved pictures
max_shots = 10 # don't collect any more pictures if we have a map
wait = False # wait for keypress

silencing_redirect = "" if verbose else ">/dev/null 2>/dev/null"
bar_width = 30 # when presenting the numbers

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
  ret = os.system("mapper_from_images %s %s 0.04 %s %s/map < /dev/null %s" % (dirname, calibration_file, dictfile, dirname, silencing_redirect))
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
      eprint("GOT THIS MANY MAP POINTS: ", num_markers.group(1))
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

real_regex = re.compile(r'(-?\d+(?:\.\d+)?)')
linscalers = [] # linear scalers for numbers coming from aruco_locate_one
linscalers_count = 0

class LinScaler:
  def __init__(self, lo, hi):
    self.lo = lo
    self.hi = hi
    assert lo < hi
    self.width = hi - lo
    self.inited = False
    self.seen_max = 0.0
    self.seen_min = 0.0
  def scale(self, curr):
    if self.inited:
      if curr > self.seen_max:
        self.seen_max = curr
      else:
        if curr < self.seen_min:
          self.seen_min = curr
    else:
      self.seen_min = curr
      self.seen_max = curr
      self.inited = True
    seen_width = self.seen_max - self.seen_min
    if seen_width == 0:
      return self.lo # avoid division by zero
    else:
      scaled = (curr - self.seen_min)/seen_width * self.width+self.lo
      return int(scaled)
    

def find_my_position(calibration_file, map_file, image_file):
  #ret = os.system("aruco_locate_one %s %s %s 2>/dev/null | grep Camera.position.as | round --zero 4" % (image_file, map_file, calibration_file))
  global linscalers
  global linscalers_count
  try:
    loc = subprocess.check_output(
            "aruco_locate_one %s %s %s 2>/dev/null" % (image_file, map_file, calibration_file),
            shell=True)
    numbers = real_regex.findall(loc)
    numbers_count = len(numbers)
    # print(loc, numbers, numbers_count, linscalers_count, file=sys.stderr)
    if numbers_count > 0:
      if linscalers_count == 0:
        linscalers = [LinScaler(0, bar_width) for i in range(numbers_count)]
        linscalers_count = numbers_count
      print("--------------------", file=sys.stderr)
      if numbers_count == linscalers_count:
        for i in range(numbers_count):
          c = linscalers[i].scale(float(numbers[i]))
          bar = ("#" * c) + (" " * (bar_width-c))
          print(("%02d: %+0.3f |%s| %+0.3f" % (i, linscalers[i].seen_min, bar, linscalers[i].seen_max)), file=sys.stderr)
  except subprocess.CalledProcessError, e:
    print(("with error: %s" % e.output), file=sys.stderr)
    loc = e.output;
  # meaning of numbers:
  # 01??? angle in frontal plane?
  # 03: angle in transversal plane (rotation around vertical axis)
  # 04: angle in sagital plane (rotation up and down)
  # 05: anterior-posterior (distance from the board)


i = 0
have_map = False # we don't have any map at hand yet
while True:
    if wait:
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
    if found > 1 or (found==1 and have_map):
      ofn = '%s/shot-%02i.jpg' % (dirname, i)
      eprint("Saving ", ofn, ", it contained ", found, " markers.")
      cv2.imwrite(ofn, img)
      # if we already have a map, find our position
      if have_map:
        find_my_position(calibration_file, dirname+"/map.yml", ofn)
      # consider recording this picture
      if found > 1 and (not have_map or i < max_shots):
        # only record more pictures with 2+ markers and if we still don't have the map
        i += 1
        # run marker mapper every now and then, to improve the map
        if i % map_every == 0:
          eprint("========= RUNNING MAPPER")
          print("Hit ctrl-C if we get stuck here", file=sys.stderr)
          have_map = run_marker_mapper(dirname)
          eprint("========= Have map? ", have_map)
    else:
      eprint("Not saving, only ", found, " markers.")
    # fi
vc.release()

if (i % map_every != 0):
  # run marker mapper, it was not run before
  run_marker_mapper(dirname)
