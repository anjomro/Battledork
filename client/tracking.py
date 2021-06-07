import cv2
import numpy as np
import imutils


class Tracking:
    lowerBound = np.array([0, 98, 189])
    upperBound = np.array([99, 219, 255])

    kernelOpen = np.ones((5, 5))
    kernelClose = np.ones((20, 20))

    def process_frame(self, frame):
        # convert BGR to HSV
        imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # create the Mask
        mask = cv2.inRange(imgHSV, self.lowerBound, self.upperBound)
        # morphology
        maskOpen = cv2.morphologyEx(mask, cv2.MORPH_OPEN, self.kernelOpen)
        maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, self.kernelClose)

        conts = cv2.findContours(maskClose, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        conts = imutils.grab_contours(conts)
        center = None

        if len(conts) > 0:
            c = max(conts, key=cv2.contourArea)
            mom = cv2.moments(c)
            center = (int(mom["m10"] / mom["m00"]), int(mom["m01"] / mom["m00"]))

        return center
