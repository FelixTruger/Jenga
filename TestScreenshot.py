import PIL
import cv2
from PIL import ImageGrab
screenShot = ImageGrab.grab()
screenShot.save("screenShot.png")

OriginalImage = cv2.imread("screenShot.png")
cv2.namedWindow("InputImage", cv2.WINDOW_NORMAL)
cv2.resizeWindow("InputImage", 1540, 810)
cv2.imshow("InputImage", OriginalImage)
cv2.waitKeyEx()