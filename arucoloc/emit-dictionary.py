#!/usr/bin/env python2
# emits one of the predefined aruco dictionaries as bits
# in the format that marker mapper needs
# Downloaded from: http://www.philipzucker.com/aruco-in-opencv/

import cv2
import cv2.aruco as aruco

'''
    drawMarker(...)
        drawMarker(dictionary, id, sidePixels[, img[, borderBits]]) -> img
'''

side = 6

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
#print(aruco_dict)
print "name aruco.DICT_6X6_250"
print "nbits", side*side
for id in range(0, 36):
  # second parameter is id number
  # last parameter is total image size
  img = aruco.drawMarker(aruco_dict, id, side+2) # the last arg is marker size, must fit the markers
  # We got the marker including border, drop it
  noborder=img[1:(side+1),1:(side+1)]
  # Flatten the marker matrix and write as 0 or 1:
  flat=[1 if i>0 else 0 for row in noborder for i in row]
  # Print as string:
  print ''.join(str(e) for e in flat)
 
# also draw the marker
# cv2.imshow('frame',img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
