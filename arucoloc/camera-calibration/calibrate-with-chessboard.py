#!/usr/bin/env python
# Downloaded from
# https://raw.githubusercontent.com/LongerVision/Examples_OpenCV/master/01_internal_camera_calibration/chessboard.py
# Changed output YAML file for the C aruco library by Ondrej Bojar

# python print to stderr (most portable and flexible)
from __future__ import print_function
import sys
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

################################################################################
#                                                                              #
#                                                                              #
#           IMPORTANT: READ BEFORE DOWNLOADING, COPYING AND USING.             #
#                                                                              #
#                                                                              #
#      Copyright [2017] [ShenZhen Longer Vision Technology], Licensed under    #
#      ******** GNU General Public License, version 3.0 (GPL-3.0) ********     #
#      You are allowed to use this file, modify it, redistribute it, etc.      #
#      You are NOT allowed to use this file WITHOUT keeping the License.       #
#                                                                              #
#      Longer Vision Technology is a startup located in Chinese Silicon Valley #
#      NanShan, ShenZhen, China, (http://www.longervision.cn), which provides  #
#      the total solution to the area of Machine Vision & Computer Vision.     #
#      The founder Mr. Pei JIA has been advocating Open Source Software (OSS)  #
#      for over 12 years ever since he started his PhD's research in England.  #
#                                                                              #
#      Longer Vision Blog is Longer Vision Technology's blog hosted on github  #
#      (http://longervision.github.io). Besides the published articles, a lot  #
#      more source code can be found at the organization's source code pool:   #
#      (https://github.com/LongerVision/OpenCV_Examples).                      #
#                                                                              #
#      For those who are interested in our blogs and source code, please do    #
#      NOT hesitate to comment on our blogs. Whenever you find any issue,      #
#      please do NOT hesitate to fire an issue on github. We'll try to reply   #
#      promptly.                                                               #
#                                                                              #
#                                                                              #
# Version:          0.0.1                                                      #
# Author:           JIA Pei                                                    #
# Contact:          jiapei@longervision.com                                    #
# URL:              http://www.longervision.cn                                 #
# Create Date:      2017-03-19                                                 #
################################################################################

import numpy as np
import cv2
import yaml


# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

cap = cv2.VideoCapture(1)
found = 0
nshots = 10
while(found < nshots):  # Here, 10 can be changed to whatever number you like to choose
    ret, img = cap.read() # Capture frame-by-frame
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (7,6), None)

    # If found, add object points, image points (after refining them)
    if ret == True and corners is not None:
        # eprint("corners: ", corners)
        objpoints.append(objp)  # Certainly, every loop objp is the same, in 3D.
        imgpoints.append(corners) # Store the found points

        # Draw and display the corners
        cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        cv2.drawChessboardCorners(img, (7,6), corners ,ret)

        # eprint("corners: ", corners)

        eprint("Found chessboard")
        found += 1

    cv2.imshow('img', img)
    cv2.waitKey(10)

eprint("Found", nshots, " shots of chessboard.")

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

eprint("Calibrating")

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

outfile="calibration.yaml"

def flatten(matrix):
  return [i for row in matrix for i in row]

eprint("Calibrated, saving:", outfile)
with open(outfile, "w") as f:
    f.write("""
%YAML:1.0
image_width: 640
image_height: 480
camera_matrix: !!opencv-matrix
   rows: 3
   cols: 3
   dt: d
   data: """)
    f.write(str(flatten(np.asarray(mtx).tolist())))
    f.write("""
distortion_coefficients: !!opencv-matrix
   rows: 1
   cols: 5
   dt: d
   data:  """)
    f.write(str(flatten(np.asarray(dist).tolist())))

