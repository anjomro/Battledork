from tracking import Tracking
from triangulation import Triangulation, Camera

import numpy as np
import cv2

if __name__ == '__main__':
    NUM_CAMS = 4
    source_list = []

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

    for i in range(NUM_CAMS):
        src = cv2.VideoCapture("Path/to/file.mp4")
        source_list.append(src)

    while True:
        no_img = False
        for i in range(NUM_CAMS):
            ret, img = source_list[i].read()
            if not ret:
                no_img = True
                break
            coordinates = tracking.process_frame(img)
            triangulation.cameras[i].ball_pos = coordinates

        if no_img:
            break

        results = triangulation.calculate_position()
