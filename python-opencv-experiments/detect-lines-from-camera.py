# import the necessary packages
import numpy as np
import cv2



def detect_lines(img):
  gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
  show = gray
  edges = cv2.Canny(gray,50,150,apertureSize = 3)
  #print img.shape[1]
  #print img.shape
  minLineLength=img.shape[1]-300
  minLineLength=200
  #lines = cv2.HoughLinesP(image=edges,rho=0.02,theta=np.pi/500, threshold=10,lines=np.array([]), minLineLength=minLineLength,maxLineGap=100)
  lines = cv2.HoughLinesP(image=edges,rho=0.2,theta=np.pi/100, threshold=10,lines=np.array([]), minLineLength=minLineLength,maxLineGap=100)
  
  if lines is not None:
    a,b,c = lines.shape
    for i in range(a):
        #cv2.line(img, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 3, cv2.LINE_AA)
        cv2.line(show, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2],
        lines[i][0][3]), (0, 0, 255), 3, cv2.CV_AA)
    return show
  else:
    return show
  #return np.hstack([edges, img])

# open video capture
cap = cv2.VideoCapture(1)
 
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    circles = detect_lines(frame)

    # Display the resulting frame
    cv2.imshow('frame',circles)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
