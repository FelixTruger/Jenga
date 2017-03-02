import cv2

OriginalImage = cv2.imread("Input\\Jenga.jpg")
cv2.namedWindow("InputImage", cv2.WINDOW_NORMAL)
cv2.resizeWindow("InputImage", 600, 600)
cv2.imshow("InputImage", OriginalImage)
cv2.waitKeyEx()