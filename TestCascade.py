import numpy as np
import cv2

jenga_cascade = cv2.CascadeClassifier('C:/Users/Michael/Documents/GitHub/Jenga/testfiles/outfiles/outputDir/cascade.xml')

img = cv2.imread('testfiles/originals/tower2.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


tower = jenga_cascade.detectMultiScale(gray, 1.3, 5)

for (x,y,w,h) in tower:
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    


cv2.namedWindow("DetectedImage", cv2.WINDOW_NORMAL)
cv2.resizeWindow("DetectedImage", 600, 600)
cv2.imshow('DetectedImage', img)
cv2.waitKey(0)
cv2.destroyAllWindows()