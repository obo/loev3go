#!/usr/bin/env python3
# From: https://gist.github.com/hauptmech/6b8ca2c05a3d935c97b1c75ec9ad85ff
# Needs to install: sudo pip2 install opencv-contrib-python
#

import numpy as np
import cv2

class ArucoFollower(object):
  """
  Runs video capture and locates aruco markers from the given dictionary.
  """

  def __init__(self, camera_index=0, arucodict=cv2.aruco.DICT_6X6_250):
    """
    Initialize to read from a camera and search for aruco markers from a
    dictionary
    """
    self.cap = cv2.VideoCapture(camera_index)
    self.dictionary = cv2.aruco.getPredefinedDictionary(arucodict)
    # other options: cv2.aruco.DICT_5X5_1000 cv2.aruco.DICT_4X4_50
    #                cv2.aruco.DICT_6X6_250 cv2.aruco.DICT_ARUCO_ORIGINAL

  def __destroy__(self):
    # When everything done, release the capture
    self.cap.release()

  def scan(self):
    ret, frame = self.cap.read()
    self.frame = frame
    self.gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    self.res = cv2.aruco.detectMarkers(self.gray,self.dictionary)
    return self.res

  def draw_detected(self, image=None):
    if image is None:
      image = self.frame
    if len(self.res[0]) > 0:
      cv2.aruco.drawDetectedMarkers(image, self.res[0], self.res[1])
    cv2.imshow('frame', image)

if __name__ == "__main__":
  """When run as script, show found markers"""
  af=ArucoFollower(1)
  while(True):
    af.scan()
    af.draw_detected()
    if cv2.waitKey(1) & 0xFF == ord('q'):
      break
  cv2.destroyAllWindows()
