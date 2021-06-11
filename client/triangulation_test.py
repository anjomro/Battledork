from triangulation import Camera, Triangulation, InsufficientDataException
import numpy as np

if __name__ == "__main__":
	# Initialise cameras and enter normalized directional vector
	camera1 = Camera(np.array([250, -275, 84]))
	camera1.normalize_direction(np.array([-211.9, 225,77, -84]))
	camera2 = Camera(np.array([250, 275, 84]))
	camera2.normalize_direction(np.array([-221.41, -223.62, -84]))
	camera3 = Camera(np.array([-250, 275, 84]))
	camera3.normalize_direction(np.array([203.077, -208.711, -84]))
	camera4 = Camera(np.array([-250, -275, 84]))
	camera4.normalize_direction(np.array([205.669, 216.506, -84]))

	triang = Triangulation([camera1, camera2, camera3, camera4])

	camera1.ball_pos = np.array([20, 60])
	camera2.ball_pos = np.array([-75, 50])
	camera3.ball_pos = np.array([48, 95])
	camera4.ball_pos = np.array([-47, 82])
	try:
		position = triang.calculate_position()
		print(position)
	except InsufficientDataException:
		print("Position could not be found because of insufficient picture data")
	wait = input("Press enter to close")
