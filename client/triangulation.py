from typing import List
import numpy as np


class Camera:
	# Position and direction of the camera lens
	POS: np.array([[float]])
	DIR: np.array([[float]])

	ball_pos: np.array([[float]])
	ball_vect: np.array([[float]])

	def __init__(self, position: np.array([[float]]), direction: np.array([[float]])):
		self.POS = position
		self.DIR = direction

	def normalize_direction(self, direction: np.array([[float]])):
		# Normalize the camera direction vector to a length of 10 cm
		length = np.sqrt(np.square(direction[0]) + np.square(direction[1]) + np.square(direction[2]))
		self.DIR = np.array([[(direction[0]/length)*10], [(direction[1]/length)*10], [(direction[2]/length)*10]])


# Class contains variables and functions for triangulation
class Triangulation:
	FACTOR_X = 1
	FACTOR_Y = 1
	NUM_CAMS = 2

	# List of available cameras
	cameras: List[Camera]

	def __init__(self, camera_list: List[Camera]):
		self.cameras = camera_list

	def calculate_position(self):
		# Empty the directions list
		self.directions.clear()
		# Calculate the directional vector of the ball
		for camera in self.cameras:
			# Horizontal picture vector
			horizontal_picture = np.cross(camera.DIR, np.array([0, 1, 0]))
			# Vertical picture vector
			vertical_picture = np.cross(camera.DIR, horizontal_picture)
			# Set length to 1
			horizontal_picture /= np.sqrt(np.square(horizontal_picture[0]) + np.square(horizontal_picture[1]) + np.square(horizontal_picture[2]))
			vertical_picture /= np.sqrt(np.square(vertical_picture[0]) + np.square(vertical_picture[1]) + np.square(vertical_picture[2]))

			# Calculate ball directional vector
			ball_direction = camera.POS + camera.DIR + np.dot(camera.ball_pos[0] * self.FACTOR_X, horizontal_picture) + np.dot(camera.ball_pos[1] * self.FACTOR_Y, vertical_picture)
			camera.ball_vect = ball_direction

		for camera1 in self.cameras:
			for camera2 in self.cameras:
				if camera1 == camera2:
					continue
				normalized = np.cross(camera1.ball_vect, camera2.ball_vect)
				# "camera1.POS + r * camera1.ball_vect + s * normalized" is a level orthogonal to both ball vectors
				# Equal it to camera2.ball_vect and we get the points on both vectors where they are closest to each other
				# r * camera1.ball_vect + s * normalized - t * camera2.ball_vect = camera2.POS - camera1.POS
				a = np.array([camera1.POS, normalized, camera2.ball_vect])
				b = np.array(camera2.POS - camera1.POS)
				result = np.linalg.solve(a, b)
				# r = result[0], s = result[1], -t = result[2]
				point1 = camera1.POS + result[0] * camera1.ball_vect
				point2 = camera2.POS - result[2] * camera2.ball_vect
				# Calculate distance between both points to check if the result is acceptable
				distance_vect = point1 - point2
				distance = np.sqrt(np.square(distance_vect[0]) + np.square(distance_vect[1]) + np.square(distance_vect[2]))
