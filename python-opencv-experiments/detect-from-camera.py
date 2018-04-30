#!/usr/bin/env python

# from https://www.pyimagesearch.com/2014/07/21/detecting-circles-images-using-opencv-hough-circles/
# import the necessary packages
import numpy as np
import cv2
from skimage.transform import hough_line, hough_line_peaks
from skimage.draw import line

dev_video = 1

def gr2bgr(image):
  return cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

cache = None
cacheindex = -1

# def detect_using_skimage(edges, background):
#   ## tohle je rozpracovana uplna blbost.
#   ## obycejny hough totiz neumi asi najit rozsahy tech usecek, ale najde
#   ## cele cary. Lepsi je pravdepodobnostni
#   ## ale ten zas nedovoluje skladat vic obrazku pres sebe, vsechno je schovane
#   ## v C
#   hspace, angles, dists = hough_line(edges)
#   #hspace, angles, dists = hough_line_peaks(hspace, angles, dists)
#   for _, angle, dist in zip(*hough_line_peaks(hspace, angles, dists)):
#     y0 = (dist - 0 * np.cos(angle)) / np.sin(angle)
#     y1 = (dist - col1 * np.cos(angle)) / np.sin(angle)
#     #ax2.plot((0, col1), (y0, y1), '-r')
#   #len(angles)
#   return hspace

def detect_lines(edges, background):
  minLineLength=edges.shape[1]-300
  #minLineLength=100
  #lines = cv2.HoughLinesP(image=edges,rho=0.02,theta=np.pi/500, threshold=10,lines=np.array([]), minLineLength=minLineLength,maxLineGap=100)
  lines = cv2.HoughLinesP(image=edges,rho=1,theta=np.pi/180,
    threshold=300,lines=np.array([]), minLineLength=20,maxLineGap=15)
  
  if lines is not None:
    show = background.copy()
    a,b,c = lines.shape
    # Crazy HoughLinesP differs in which axis are lines listed:
    # https://stackoverflow.com/questions/29872439/opencv-houghlines-only-ever-returning-one-line
    #print lines, a, b, c
    i=0
    for j in range(b):
        #cv2.line(show, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 3, cv2.LINE_AA)
        cv2.line(show, (lines[i][j][0], lines[i][j][1]), (lines[i][j][2],
        lines[i][j][3]), (0, 0, 255), 3, cv2.CV_AA)
    return show
  else:
    return background

def detect_circles(gray, background):
  #circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1.2, 100)
  circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1.9, 200)
   
  # ensure at least some circles were found
  if circles is not None:
    # convert the (x, y) coordinates and radius of the circles to integers
    circles = np.round(circles[0, :]).astype("int")
    output = background.copy()
   
    # loop over the (x, y) coordinates and radius of the circles
    for (x, y, r) in circles:
      print("circle: ", x, y, r)
      # draw the circle in the output image, then draw a rectangle
      # corresponding to the center of the circle
      cv2.circle(output, (x, y), r, (0, 255, 0), 4)
      cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
    return output
  else:
    return background

def process_and_show(image):
  blur = cv2.bilateralFilter(image,9,75,75)
  #B = blur
  #C = cv2.GaussianBlur(image,(5,5),0)
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  global cache
  global cacheindex
  if cache is None:
    cache = np.stack([gray, gray, gray, gray, gray, gray, gray, gray, gray,
      gray])
    cacheindex = 0
  else:
    # cache is a rotating buffer
    cache[cacheindex,:] = gray
    cacheindex = (cacheindex+1) % 10

  avg = np.mean(cache, axis=0)
  avgint = avg.astype(np.uint8)
  #equ = cv2.equalizeHist(gray)
  #clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
  #cla = clahe.apply(gray)
  edg = cv2.Canny(avgint,50,150,apertureSize = 3)
  #C = gr2bgr(edg)

  # what to show:
  A = image
  #B = gr2bgr(cla)
  #B = gr2bgr(gray)
  #B = blur
  #C = gr2bgr(equ)
  #D = detect_circles(gray, image)
  B = gr2bgr(avgint)
  #C = gr2bgr(edg)
  kernel = np.ones((10,10), np.uint8)
  dil = cv2.dilate(edg, kernel, iterations=1)
  C = gr2bgr(dil)
  D = detect_lines(dil, image)
  # D = detect_using_skimage(edg, image)
  
  # show four images
  return np.vstack([
    np.hstack([A, B]),
    np.hstack([C, D])
  ])

# open video capture
cap = cv2.VideoCapture(dev_video)
 
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    show = process_and_show(frame)

    # Display the resulting frame
    cv2.imshow('frame',show)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
