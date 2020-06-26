import cv2 as cv
import numpy as np
import datetime
import os
from constants import ORIGINAL, MODIFIED
from utils import getFilePath

def findAcc(path):
	img = cv.imread(getFilePath(ORIGINAL, path))
	low_green = np.array([0, 80, 0])
	high_green = np.array([150, 255, 100])
	hsv_img = cv.cvtColor(img, cv.COLOR_BGR2HSV)

	mask = cv.inRange(hsv_img, low_green, high_green)
	res = cv.bitwise_and(img, img, mask = mask)
	# cv.imwrite(nam + " Mask.png", mask)

	bw = cv.cvtColor(res, cv.COLOR_BGR2GRAY)
	bw = cv.GaussianBlur(bw, (3, 3), 0)


	a, thresh = cv.threshold(bw, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
	kernel = np.ones((5,5), np.uint8)
	
	canny = cv.Canny(bw, a*0.5, a)
	# cv.imwrite(nam + " Canny.png", canny)

	canny = cv.dilate(canny, kernel, iterations=1)
	# cv.imwrite(nam + " Dilated.png", canny)
	# cv.imshow("ss", canny)
	
	area, tot = cv.countNonZero(canny), img.shape[0] * img.shape[1]
	date = datetime.datetime.now()
	cv.putText(img, 'Forest Cover ' + str(area/tot * 100) , (56, 80), cv.FONT_HERSHEY_COMPLEX, 0.7, (2,255,2),2)
	cv.putText(img, str(date.day) + '/' + str(date.month) + '/' + str(date.year) , (600, 500), cv.FONT_HERSHEY_COMPLEX, 0.7, (2,255,2),2)
	
	cv.imwrite(getFilePath(MODIFIED, path), img)
	return area/tot



# img = cv.imread('img2.png')

# findAcc(img, 3)
# img = cv.imread('original.png')

# findAcc(img, 6)

cv.waitKey(0)
cv.destroyAllWindows()
