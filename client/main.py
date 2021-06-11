from tracking import Tracking
from triangulation import Triangulation, Camera, InsufficientDataException
from statistics import Statistics

import time
import numpy as np
import cv2

# Taken from https://stackoverflow.com/questions/3173320/text-progress-bar-in-the-console
# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


if __name__ == '__main__':
    NUM_CAMS = 4
    # List of video sources
    source_list = []
    # List will contain points of the flying curve
    ball_curve = []

    camera1 = Camera(np.array([250, -275, 84]))
    camera1.normalize_direction(np.array([-225.082, 233.359, -84]))
    camera2 = Camera(np.array([250, 275, 84]))
    camera2.normalize_direction(np.array([-235.76, -230.35, -84]))
    camera3 = Camera(np.array([-250, 275, 84]))
    camera3.normalize_direction(np.array([203.077, -208.711, -84]))
    camera4 = Camera(np.array([-250, -275, 84]))
    camera4.normalize_direction(np.array([205.669, 216.506, -84]))

    tracking = Tracking()
    triangulation = Triangulation([camera1, camera2, camera3, camera4])
    filename = "Battledork_180s_tonic-tradition__2021-05-30+18 40 33__{}.h264"

    frame_counter = 0

    for i in range(NUM_CAMS):
        src = cv2.VideoCapture(filename.format(i))
        source_list.append(src)
        ret, first_img = src.read()
        first_HSV = cv2.cvtColor(first_img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(first_HSV, tracking.lowerBound, tracking.upperBound)
        tracking.background_list.append(mask)


    while True:
        no_img = False
        for i in range(NUM_CAMS):
            ret, img = source_list[i].read()
            # ret is false if no more frames available
            if not ret:
                no_img = True
                break
            # Get ball coordinates in frame
            coordinates_tuple = tracking.process_frame(img, i)
            # If ball was not found, set boolean in camera. Else, write coordinates to camera
            current_cam = triangulation.cameras[i]
            if coordinates_tuple is None:
                current_cam.not_found = True
            else:
                coordinates = np.array([coordinates_tuple[0] - 640, (coordinates_tuple[1] - 360) * -1])
                current_cam.not_found = False
                current_cam.ball_pos = coordinates

        # Break out of the loop if no more frames are provided
        if no_img:
            break

        # Calculate ball position from camera angles
        try:
            ball_curve.append(triangulation.calculate_position())
            frame_counter += 1
            printProgressBar((frame_counter/80), 180, prefix="Progress:", length=50)
        except InsufficientDataException:
            # Fill curve with impossible position
            ball_curve.append(np.array([[0], [0], [-10]]))
            frame_counter += 1
            printProgressBar((frame_counter/80), 180, prefix="Progress:", length=50)

    print(ball_curve)

    stats = Statistics(ball_curve)
    print(stats.count_hits())
