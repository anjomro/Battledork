from triangulation import Camera, Triangulation, InsufficientDataException
import numpy as np

if __name__ == "__main__":
	# Initialise cameras and enter normalized directional vector
	camera1 = Camera(np.array([-100, -100, 100]))
	camera1.normalize_direction(np.array([1, 1, 0]))
	camera2 = Camera(np.array([-100, 100, 100]))
	camera2.normalize_direction(np.array([1, -1, 0]))
	triang = Triangulation([camera1, camera2])

	camera1.ball_pos = np.array([0, -1])
	camera2.ball_pos = np.array([0, -0.9999999])
	try:
		position = triang.calculate_position()
		print(position)
	except InsufficientDataException:
		print("Position could not be found because of insufficient picture data")
	wait = input("Press enter to close")
