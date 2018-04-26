




# from https://www.pyimagesearch.com/2014/07/21/detecting-circles-images-using-opencv-hough-circles/
# import the necessary packages
import numpy as np
import cv2



def detect_circles(image):
  gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
  show = gray
  
  # detect circles in the image
  #circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1.2, 100)
  circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1.9, 200)
   
  # ensure at least some circles were found
  if circles is not None:
    # convert the (x, y) coordinates and radius of the circles to integers
    circles = np.round(circles[0, :]).astype("int")
    output = show.copy()
   
    # loop over the (x, y) coordinates and radius of the circles
    for (x, y, r) in circles:
      print("circle: ", x, y, r)
      # draw the circle in the output image, then draw a rectangle
      # corresponding to the center of the circle
      cv2.circle(output, (x, y), r, (0, 255, 0), 4)
      cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
    return np.hstack([show, output])
  else:
    return np.hstack([show, show])

# open video capture
cap = cv2.VideoCapture(0)
 
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    circles = detect_circles(frame)

    # Display the resulting frame
    cv2.imshow('frame',circles)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
