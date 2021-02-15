import cv2
import numpy as np
import imutils
import time
import sys

lowerBound = np.array([0, 98, 189])
upperBound = np.array([99, 219, 255])

source = 0
if len(sys.argv) > 1:
	source = sys.argv[1]
cam = cv2.VideoCapture(source)
kernelOpen = np.ones((5, 5))
kernelClose = np.ones((20, 20))

font = cv2.FONT_HERSHEY_SIMPLEX

frame_counter = 0
total_time = 0

print("running...")

try:
	while True:
		start_time = time.time()
		ret, img = cam.read()
		if ret == False:
			break
		#img = cv2.resize(img, (340, 220))

		# convert BGR to HSV
		imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		# create the Mask
		mask = cv2.inRange(imgHSV, lowerBound, upperBound)
		# morphology
		maskOpen = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernelOpen)
		maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, kernelClose)

		#maskFinal = maskClose
		conts = cv2.findContours(maskClose, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
		conts = imutils.grab_contours(conts)
		center = None

		if len(conts) > 0:
			c = max(conts, key=cv2.contourArea)
			#((x, y), radius) = cv2.minEnclosingCircle(c)
			M = cv2.moments(c)
			center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
			#cv2.circle(img, (int(x), int(y)), int(radius), (0, 255, 255), 2)
			#cv2.circle(img, center, 5, (0, 0, 255), -1)

		'''
		cv2.drawContours(img, conts, -1, (255, 0, 0), 3)
		for i in range(len(conts)):
			x, y, w, h = cv2.boundingRect(conts[i])
			cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
			cv2.putText(img, str(i + 1), (x, y + h), font, 1, (0, 255, 255))
		'''
		#cv2.imshow("maskClose", maskClose)
		#cv2.imshow("maskOpen", maskOpen)
		#cv2.imshow("mask", mask)
		#cv2.imshow("cam", img)
		#cv2.waitKey(1)
		frame_counter += 1
		total_time += (time.time() - start_time) * 1000

finally:
	print("Possible FPS:", round(1000 / (total_time / frame_counter)))
