import cv2
import numpy as np
import imutils


class Tracking:
    background_list = []

    lowerBound = np.array([0, 98, 189])
    upperBound = np.array([99, 219, 255])

    kernelOpen = np.ones((5, 5))
    kernelClose = np.ones((20, 20))

    previous_frame = None

    def process_frame(self, frame, cam_index):
        # Fill variable
        subMask = self.background_list[cam_index]
        # convert BGR to HSV
        imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # create the Mask
        mask = cv2.inRange(imgHSV, self.lowerBound, self.upperBound)
        cv2.subtract(mask, self.background_list[cam_index], subMask)
        # morphology
        maskOpen = cv2.morphologyEx(subMask, cv2.MORPH_OPEN, self.kernelOpen)
        maskClose = cv2.morphologyEx(maskOpen, cv2.MORPH_CLOSE, self.kernelClose)

        conts = cv2.findContours(maskClose, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        conts = imutils.grab_contours(conts)
        center = None

        if len(conts) > 0:
            c = max(conts, key=cv2.contourArea)
            mom = cv2.moments(c)
            center = (int(mom["m10"] / mom["m00"]), int(mom["m01"] / mom["m00"]))
            cv2.drawContours(frame, c, -1, (255, 0, 0), 3)

        # cv2.imshow("Camera {}".format(cam_index), frame)
        # cv2.waitKey(1)

        self.background_list[cam_index] = mask

        return center