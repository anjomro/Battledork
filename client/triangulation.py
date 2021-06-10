from typing import List
import numpy as np


class Camera:
    # Position and direction of the camera lens
    POS: np.array([[float]])
    DIR: np.array([[float]])

    ball_pos: np.array([[float]])
    ball_vect: np.array([[float]])

    not_found: bool = False

    def __init__(self, position: np.array([[float]])):
        self.POS = position

    def normalize_direction(self, direction: np.array([[float]])):
        # Normalize the camera direction vector to a length of 10 cm
        length = np.sqrt(np.square(direction[0]) + np.square(direction[1]) + np.square(direction[2]))
        self.DIR = np.array([(direction[0] / length) * 10, (direction[1] / length) * 10, (direction[2] / length) * 10])


class InsufficientDataException(BaseException):
    pass


# Class contains variables and functions for triangulation
class Triangulation:
    FACTOR_X = 1/138
    FACTOR_Y = 1/138

    # List of available cameras
    cameras: List[Camera]

    results = []

    def __init__(self, camera_list: List[Camera]):
        self.cameras = camera_list

    def calculate_position(self):
        # Empty the results List
        self.results.clear()
        # Calculate the directional vector of the ball
        for camera in self.cameras:
            # Continue if ball is invisible for current camera
            if camera.not_found:
                continue
            # Horizontal picture vector
            horizontal_picture = np.cross(camera.DIR, np.array([0, 0, 1]), axis=0)
            # Vertical picture vector
            vertical_picture = np.cross(horizontal_picture, camera.DIR, axis=0) / 100

            # Calculate ball directional vector
            ball_direction = camera.DIR + (camera.ball_pos[0] * self.FACTOR_X) * horizontal_picture + (
                    camera.ball_pos[1] * self.FACTOR_Y) * vertical_picture
            camera.ball_vect = ball_direction

        for camera1 in self.cameras:
            if camera1.not_found:
                continue
            for camera2 in self.cameras:
                if (camera1 == camera2) or camera2.not_found:
                    continue
                normalized = np.cross(camera1.ball_vect, camera2.ball_vect)
                # "camera1.POS + r * camera1.ball_vect + s * normalized" is a plane orthogonal to both ball vectors
                # Equal it to camera2.ball_vect and we get the points on both vectors where they are closest to each other
                # r * camera1.ball_vect + s * normalized - t * camera2.ball_vect = camera2.POS - camera1.POS
                A = np.array([[camera1.ball_vect[0], normalized[0], -camera2.ball_vect[0]],
                              [camera1.ball_vect[1], normalized[1], -camera2.ball_vect[1]],
                              [camera1.ball_vect[2], normalized[2], -camera2.ball_vect[2]]])
                b = np.array(camera2.POS - camera1.POS)
                result = np.linalg.solve(A, b)
                # result = [r, s, t]
                point1 = camera1.POS + camera1.ball_vect * result[0]
                point2 = camera2.POS + camera2.ball_vect * result[2]
                dist_vect = point1 - point2
                length = np.sqrt(np.square(dist_vect[0]) + np.square(dist_vect[1]) + np.square(dist_vect[2]))
                if length < 10:
                    self.results.append(point1)
                    self.results.append(point2)

        # Return false in case no accurate position could be calculated
        if self.results.__len__() < 1:
            raise InsufficientDataException
        else:
            # Calculate the average of all results
            average = self.results[0]
            for vector in self.results[1:]:
                average += vector
            average /= self.results.__len__()
            return average
