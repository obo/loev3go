#!/usr/bin/env python
# Run on robot (or notebook)
# Have mapper_from_images (from marker_mapper) in your path
# It will take a picture at every return key
# It will try to build a map at every X collects.

# python print to stderr (most portable and flexible)
from __future__ import print_function
import sys
verbose = True
debug = True
def eprint(*args, **kwargs):
    if verbose: print(*args, file=sys.stderr, **kwargs)
def dprint(*args, **kwargs):
    if debug: print(*args, file=sys.stderr, **kwargs)
show_shots = False # show shots in a window

import datetime
import numpy as np
import cv2
import os
import re
import subprocess
import time

camera = 0
calibration_file = "calibration.yaml"
dictfile = "DICT_6x6_250.dict"
map_every = 3 # try marker_mapper every 5 saved pictures
max_shots = 10 # don't collect any more pictures if we have a map
min_delay = 2000/1000 # seconds between accepted frames
wait = False # wait for keypress

silencing_redirect = "" if verbose else ">/dev/null 2>/dev/null"
bar_width = 30 # when presenting the numbers

# check if prerequisites are found
assert(os.system("which mapper_from_images") == 0)
assert(os.system("which aruco_locate_one") == 0)


# create timestamped directory
d = datetime.datetime.now() 
ts = '%04d%02d%02d-%02d%02d%02d' % (d.year, d.month, d.day, d.hour, d.minute, d.second)
dirname = "shots-"+ts
os.mkdir(dirname)

# prepare image capturing
vc = cv2.VideoCapture(camera)

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
  def __init__(self, lo, hi, centered=False):
    self.lo = lo
    self.hi = hi
    self.centered = centered
    assert lo < hi
    self.width = hi - lo
    self.inited = False
    self.seen_max = 0.0
    self.seen_min = 0.0
  def update_seen_one_dir(self, curr):
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
  def update_seen(self, curr):
    self.update_seen_one_dir(curr)
    if self.centered: self.update_seen_one_dir(-curr)
  def scale(self, curr):
    self.update_seen(curr)
    seen_width = self.seen_max - self.seen_min
    if seen_width == 0:
      return self.lo # avoid division by zero
    else:
      scaled = (curr - self.seen_min)/seen_width * self.width+self.lo
      return int(scaled)
    
class Pose:
  def __init__(self, rvec, tvec):
    self.rvec = rvec
    self.tvec = tvec
  def relative_to(self, NewHome):
    # code from:
    # https://github.com/aliyasineser/GraduationProjectII/blob/master/RelativePositionTest.py
    def inversePerspective(rvec, tvec):
      R, _ = cv2.Rodrigues(rvec)
      R = np.matrix(R).T
      invTvec = np.dot(-R, np.matrix(tvec))
      invRvec, _ = cv2.Rodrigues(R)
      return invRvec, invTvec
    def relativePosition(rvec1, tvec1, rvec2, tvec2):
      rvec1, tvec1 = rvec1.reshape((3, 1)), tvec1.reshape((3, 1))
      rvec2, tvec2 = rvec2.reshape((3, 1)), tvec2.reshape((3, 1))
      # Inverse the second marker, the right one in the image
      invRvec, invTvec = inversePerspective(rvec2, tvec2)
      orgRvec, orgTvec = inversePerspective(invRvec, invTvec)
      # print("rvec: ", rvec2, "tvec: ", tvec2, "\n and \n", orgRvec, orgTvec)
      info = cv2.composeRT(rvec1, tvec1, invRvec, invTvec)
      composedRvec, composedTvec = info[0], info[1]
      composedRvec = composedRvec.reshape((3, 1))
      composedTvec = composedTvec.reshape((3, 1))
      return composedRvec, composedTvec
    transformedRvec, transformedTvec = relativePosition(self.rvec, self.tvec, NewHome.rvec, NewHome.tvec)
    return Pose(transformedRvec, transformedTvec)
  def __str__(self):
    return "R%s T%s" % (self.rvec.transpose(), self.tvec.transpose())

def find_my_position(calibration_file, map_file, image_file):
  #ret = os.system("aruco_locate_one %s %s %s 2>/dev/null | grep Camera.position.as | round --zero 4" % (image_file, map_file, calibration_file))
  try:
    loc = subprocess.check_output(
            "aruco_locate_one %s %s %s 2>/dev/null" % (image_file, map_file, calibration_file),
            shell=True)
    # Output of aruco_locate_one has this format:
    # Camera position as getRvec, getTvec: [2.174823, 2.0144002, -0.48945314] [0.20740934, -0.11405521, 0.84579444]
    # Camera position as TUM RGBD: 0 0.372795 -0.115674 0.78679 0.722148 0.66888 -0.162522 -0.0684754
    numbers = [float(s) for s in real_regex.findall(loc)]
    numbers_count = len(numbers)
    if numbers_count == 14:
      # assume the format was correct, get rvec
      rvec = numbers[0:3]
      tvec = numbers[3:6]
      return Pose(np.array(rvec), np.array(tvec))
  except subprocess.CalledProcessError, e:
    print(("with error: %s" % e.output), file=sys.stderr)
    loc = e.output;
  # meaning of numbers:
  # 01??? angle in frontal plane?
  # 03: angle in transversal plane (rotation around vertical axis)
  # 04: angle in sagital plane (rotation up and down)
  # 05: anterior-posterior (distance from the board)
  #
  # I could not find any other. That's because 00--05 and 07--13 are
  # equivalent to each other and each of them alone expresses the 3D pose of
  # the camera with respect to some random coordinate system.
  # What I need to figure out is how to do a diff of two camera poses, i.e.
  # when setting one of the poses as "home", how to express the other one
  # with respect to this home.

def plot_numbers(numbers):
  # plot numbers using linscalers
    # print(loc, numbers, numbers_count, linscalers_count, file=sys.stderr)
  global linscalers
  global linscalers_count
  dprint(numbers)
  numbers_count = len(numbers)
  if numbers_count > 0:
    if linscalers_count == 0:
      linscalers = [LinScaler(0, bar_width, centered=True) for i in range(numbers_count)]
      linscalers_count = numbers_count
    print("--------------------", file=sys.stderr)
    if numbers_count == linscalers_count:
      for i in range(numbers_count):
        c = linscalers[i].scale(numbers[i])
        bar = ("#" * c) + (" " * (bar_width-c))
        print(("%02d: %+0.3f |%s| %+0.3f" % (i, linscalers[i].seen_min, bar, linscalers[i].seen_max)), file=sys.stderr)


# motion blur detection by variance of Laplacian
# https://www.pyimagesearch.com/2015/09/07/blur-detection-with-opencv/
blur_threshold = 100.0

i = 0
lastkey = None
home_pose = None
have_map = False # we don't have any map at hand yet
save_only_at = time.time() + min_delay
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
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Check blurriness
    gray2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.Laplacian(gray2, cv2.CV_64F).var()
    if blur < blur_threshold:
      cv2.imshow('blur',gray)
      lastkey = cv2.waitKey(1) # to update displays
      continue
    # cv2.imshow('nonblur',gray)

    eprint("Checking if it contains markers.")
    res = cv2.aruco.detectMarkers(gray, dictionary)
    found = len(res[0])
    if found > 1 or (found==1 and have_map):
      ofn = '%s/shot-%02i.jpg' % (dirname, i)
      eprint("Saving ", ofn, ", it contained ", found, " markers.")
      cv2.imwrite(ofn, img)
      # show the image with markers
      if show_shots:
        cv2.aruco.drawDetectedMarkers(img,res[0],res[1])
        cv2.imshow('frame',img)
      # if we already have a map, find our position
      if have_map:
        pose = find_my_position(calibration_file, dirname+"/map.yml", ofn)
        # if space was hit, set our home
        if lastkey == 32:
          home_pose = pose
          dprint("Set home to: ", home_pose)
        else:
          if home_pose is not None:
            try:
              pose_wrt_home = pose.relative_to(home_pose)
              dprint(pose_wrt_home)
              dprint(pose_wrt_home.rvec)
              rlist = pose_wrt_home.rvec.transpose().tolist()[0]
              dprint(rlist)
              tlist = pose_wrt_home.tvec.transpose().tolist()[0]
              dprint(tlist)
              plot_numbers(rlist+tlist)
              # plot_numbers(pose_wrt_home.rvec.transpose().tolist()+pose_wrt_home.tvec.transpose().tolist())
            except Exception as e:
              dprint("Transformation failed for %s wrt to %s." % (pose, home_pose))
              dprint(e)

      # consider recording this picture
      if found > 1 and (not have_map or i < max_shots) and time.time() > save_only_at:
        # only record more pictures with 2+ markers and if we still don't have
        # the map and sufficient time has passed between the shots
        i += 1
        save_only_at = time.time() + min_delay;
        sys.stderr.write(".")
        # run marker mapper every now and then, to improve the map
        if i % map_every == 0:
          eprint("========= RUNNING MAPPER")
          print("Hit ESC if we get stuck here", file=sys.stderr)
          have_map = run_marker_mapper(dirname)
          eprint("========= Have map? ", have_map)
    else:
      eprint("Not saving, only ", found, " markers.")
      # Draw it for debugging
      if show_shots:
        cv2.imshow('frame',img)
    # fi
    if show_shots:
      lastkey = cv2.waitKey(1) # to update displays
vc.release()

if (i % map_every != 0):
  # run marker mapper, it was not run before
  run_marker_mapper(dirname)
