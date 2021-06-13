from tracking import Tracking
from triangulation import Triangulation, Camera, InsufficientDataException
from statistics import Statistics

import numpy as np
import cv2
import yaml

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

    print("Welcome to the table tennis ball tracking system\n")
    print("Reading config...")

    back_sub = False
    show_images = False
    NUM_CAMS = 0
    factor = 1
    res_x = 1
    res_y = 1
    fps = 1
    total_frames = 0

    # Read data from config.yaml file
    try:
        with open("config.yaml", 'r') as stream:
            data = yaml.safe_load(stream)
        NUM_CAMS = data['NUM_CAMS']
        show_images = data['Show_Images']
        back_sub = data['Back_Sub']
        factor = data['Factor']
        res_x = data['Res_X']
        res_y = data['Res_Y']
        fps = data['FPS']
    except yaml.YAMLError as e:
        print(e)
        exit()

    # List of video sources
    source_list = []
    # List will contain points of the flying curve
    ball_curve = []

    tracking = Tracking()
    triangulation = Triangulation()
    triangulation.FACTOR_X = 1/factor
    triangulation.FACTOR_Y = 1/factor

    # filename = "Battledork_180s_tonic-tradition__2021-05-30+18 40 33__{}.h264"
    print("Please enter the name of your files (replace number with '{}')")
    filename = input("File: ")

    frame_counter = 0

    print("Preparing cameras...")

    for i in range(NUM_CAMS):
        src = cv2.VideoCapture("videos/" + filename.format(i))
        source_list.append(src)

        cam_data = data['Camera_{}'.format(i+1)]
        # Skip number of frames set in config
        src.set(cv2.CAP_PROP_POS_FRAMES, cam_data['Skip_frames'])
        # Create camera object from config
        camera = Camera(np.array(cam_data['POS']))
        camera.normalize_direction(np.array(cam_data['DIR']))
        triangulation.cameras.append(camera)

        # Read first frame and apply background mask
        ret, first_img = src.read()
        first_HSV = cv2.cvtColor(first_img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(first_HSV, tracking.lowerBound, tracking.upperBound)
        # Store first background in tracking object
        tracking.background_list.append(mask)

    # Get total number of frames for progress bar
    total_frames = int(source_list[0].get(cv2.CAP_PROP_FRAME_COUNT))

    print("Starting (this might take a while)...")

    while True:
        no_img = False
        for i in range(NUM_CAMS):
            ret, img = source_list[i].read()
            # ret is false if no more frames available
            if not ret:
                no_img = True
                break
            # Get ball coordinates in frame
            coordinates_tuple = tracking.process_frame(img, i, back_sub, show_images)
            # If ball was not found, set boolean in camera. Else, write coordinates to camera
            current_cam = triangulation.cameras[i]
            if coordinates_tuple is None:
                current_cam.not_found = True
            else:
                coordinates = np.array([coordinates_tuple[0] - res_x/2, (coordinates_tuple[1] - res_y/2) * -1])
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

        frame_counter += 1
        printProgressBar(frame_counter, total_frames, prefix="Progress:", length=50)

    stats = Statistics(ball_curve)
    print("\n\nStatistics:\n")
    print("Hit counter: {}".format(stats.count_hits()))
    print("Max. speed: {0:.2f} m/s".format(stats.max_speed(fps)))
    input()
