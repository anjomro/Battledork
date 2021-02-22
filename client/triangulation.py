from vectors import Point, Vector


class Camera:
	# Position and direction of the camera lens
	POS = None
	DIR = None

	ballVector = None

	def __init__(self, position, direction):
		self.POS = position
		self.DIR = direction

	def setPosition(self, x, y, z):
		self.POS = Point(x, y, z)


# Class contains variables and functions for triangulation
class Triang:
	FACTOR_X = 1
	FACTOR_Y = 1

	# List of available cameras
	cameras = None

	# Store start and end points of vector lines for calculation
	points = None

	def __init__(self, cameraList):
		self.cameras = cameraList

	def calculatePosition(self):
		for camera in self.cameras:
			# Add points to draw a line from the camera in the direction of the ball
			self.points.append(camera.POS)
			# Ball is estimated to stay within 5m of the camera, hence the 500cm length
			self.points.append(camera.POS.sum(camera.ballVector.multiply(500)))

	def findIntersection(self, ):
		#TODO: Find point where lines are at minimum distance
