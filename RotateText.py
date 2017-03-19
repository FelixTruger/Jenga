import cv2
import numpy as np

#Create output window
cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Image", 1000, 1000)

img = cv2.imread('Input\Text_4_90.png')


cv2.imshow("Image", img)
cv2.waitKey(0)


#Convert image to grey and 
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.bitwise_not(gray)


#Binarize the image with an automatic generarted OTSU threshold
#OTSU -> Generates threshold based on brightness of the input image
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

cv2.imshow("Image", thresh)
cv2.waitKey(0)


#Detect edges with a canny edge detection
canny = cv2.Canny(gray, 50, 200, 3)

#Picture 3 canny threshholds
#canny = cv2.Canny(gray, 150, 1350, 3)

cv2.imshow("Image", canny)
cv2.waitKey(0)

#Find all lines in the image
#The threshold must be relative high, because otherwise the letters themself will
#be recognized as lines and not only the text lines (L will return 2 lines with a low threshold)

useHoughLineP = False

if useHoughLineP:
    lines = cv2.HoughLinesP(canny, 1, 3.1415/180, 250, 50, 10)
else:
    lines = cv2.HoughLines(canny, 1, 3.1415/180, 250, 50, 0)

    #Picture 4 hough trheshhold
    #lines = cv2.HoughLines(canny, 1, 3.1415/180, 125, 50, 0)

#Generate array for all the angles
angles = np.zeros(lines.shape[0])


for i in range(0, lines.shape[0]):
    if useHoughLineP:
        #HoughP returns points that can be used to draw the found lines
        p1x = lines[i][0][0]
        p1y = lines[i][0][1]
        p2x = lines[i][0][2]
        p2y = lines[i][0][3]
    else:
        #Hough returns points in polar coordinates
        #Part with sin and cos recreates a line on the point with the right angle
        rho = lines[i][0][0]
        theta = lines[i][0][1]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        p1x = (x0 + (-b))
        p1y = (y0 + (a))
        p2x = (x0 - (-b))
        p2y = (y0 - (a))

    #If p2x == p1x the calculation of the rising of the line would fail
    #(p2y - p1y) / (p2x - p1x) -> (p2y - p1y) / 0
    #If these two are the same, then the found line is 90° because it is parallel to the y-axis
    if p2x - p1x == 0:
        angles[i] = 90
        rise = None
    else:
        #Normiere die Steigung auf 1 um den Winkel der Linie auszurechnen
        #arccos( 1 / sqrt( 1^2 + steigerung^2 ) )
        rise = (p2y - p1y) / (p2x - p1x)
        length = np.sqrt(np.power(1, 2) + np.power(rise, 2))
        angles[i] = np.round(np.arccos(1 / length) * 180 / 3.1415)


    #Draw the found lines
    #To make the lines visible these lines should be long
    #If the angle is 90° just draw a big line parallel to the y-axis
    #Otherwise go with p1 1000 steps back and with p2 1000 steps forward and draw the line between the points
    #p1x = 0, p1y = 10, rise = 1 -> p1x = 0 - 1000, p1y = 10 - 1000 * 1
    if rise is None:
        cv2.line(canny, (int(p1x), int(p1y - 1000)), (int(p2x), int(p2y + 1000)), (255, 255, 255), 1)
    else:
        cv2.line(canny, (int(p1x - 1000), int(p1y - 1000 * rise)), (int(p2x + 1000), int(p2y + 1000 * rise)), (255, 255, 255), 1)
            

cv2.imshow("Image", canny)
cv2.waitKey(0)

#Create a histogram with the found angles
angleHistogram = np.zeros(181)
mostCommonAngleCount = -1
mostCommonAngle = 0

#Determine the most common angle found
#Eliminate angles that are out of bound, but normally arccos does that [Region of Values of arccos = [-90, 90]]
for i in range(0, angles.shape[0]):
    if(angles[i] > 90):
        angles[i] = 90
    if(angles[i] < -90):
        angles[i] = -90
    angleHistogram[int(angles[i] + 90)] = angleHistogram[int(angles[i] + 90)] + 1

    if(angleHistogram[int(angles[i] + 90)] > mostCommonAngleCount):
        mostCommonAngle = angles[i]
        mostCommonAngleCount = angleHistogram[int(angles[i] + 90)]

#Check if the image is right or left tilted and change the angle to the tilt
if mostCommonAngle > 0:
    mostCommonAngle = mostCommonAngle * -1

#Create a rotation matrix and apply this rotation matrix on the original image
rows, cols = canny.shape
rotateMatrix = cv2.getRotationMatrix2D((cols/2, rows/2), mostCommonAngle, 1)
rotatedImage = cv2.warpAffine(img, rotateMatrix, (cols, rows))


cv2.imshow("Image", rotatedImage)
cv2.waitKey(0)