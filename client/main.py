from tracking import Tracking
from triangulation import Triangulation, Camera, InsufficientDataException
from statistics import Statistics

import numpy as np
import cv2

if __name__ == '__main__':
    NUM_CAMS = 4
    # List of video sources
    source_list = []
    # List will contain points of the flying curve
    ball_curve = []

    camera1 = Camera(np.array([[1.0], [1.0], [1.0]]))
    camera1.DIR = np.array([[1.0], [0.0], [1.0]])
    camera2 = Camera(np.array([[1.0], [1.0], [1.0]]))
    camera2.DIR = np.array([[1.0], [0.0], [1.0]])
    camera3 = Camera(np.array([[1.0], [1.0], [1.0]]))
    camera3.DIR = np.array([[1.0], [0.0], [1.0]])
    camera4 = Camera(np.array([[1.0], [1.0], [1.0]]))
    camera4.DIR = np.array([[1.0], [0.0], [1.0]])

    tracking = Tracking()
    triangulation = Triangulation([camera1, camera2, camera3, camera4])
    filename = "Battledork_180s_tonic-tradition_2021-05-30+18:40:33_"

    for i in range(NUM_CAMS):
        src = cv2.VideoCapture(filename + "_" + i)
        source_list.append(src)

    while True:
        no_img = False
        for i in range(NUM_CAMS):
            ret, img = source_list[i].read()
            # ret is false if no more frames available
            if not ret:
                no_img = True
                break
            # Get ball coordinates in frame
            coordinates = tracking.process_frame(img)
            # If ball was not found, set boolean in camera. Else, write coordinates to camera
            current_cam = triangulation.cameras[i]
            if coordinates is None:
                current_cam.not_found = True
            else:
                current_cam.not_found = False
                current_cam.ball_pos = coordinates

        # Break out of the loop if no more frames are provided
        if no_img:
            break

        # Calculate ball position from camera angles
        try:
            ball_curve.append(triangulation.calculate_position())
        except InsufficientDataException:
            # Fill curve with impossible position
            ball_curve.append(np.array([[0], [0], [-10]]))

    print(ball_curve)

    stats = Statistics(ball_curve)
    hits = stats.count_hits()
    print(hits)
