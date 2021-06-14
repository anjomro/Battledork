# Battledork
*Tabletennis Tracking Program*
###### (Initially made for Badminton, hence the name)

## Usage
At least two different angles need to be recorded for the program to work properly. It is recommended to have around four cameras to cover most ball positions. The program detects the ball based on it's orange colour. This means that for proper results, no other objects in the orange colour spectrum should be close to the camera view.

The recordings should be placed in a "videos" subfolder inside the client directory. The program supports many file types, but has been tested with the direct .h264 output of Raspberry Pi cameras. The files should all share the same name and have a number at the end. This number attaches a video to a camera and starts at 0. For example, the following file names are possible:

- tabletennis_recording_filename_0.h264
- tabletennis_recording_filename_1.h264
- ...

The config.yaml file contains the camera configuration data and offers some more options for the program. Position and direction for each camera has to be set in the file. The coordinates originate from the center of the table at table top height and uses centimeters. First dimension parallel to the table width, second is relative to the table length and the third coordinate marks the height. For example, a camera placed at 250 cm to the right of the table center and 275 cm backwards at a height of 1,60 m above the ground would have the coordinates (250, -275, 84). The camera direction is given as a vector in the same format. If the camera is aimed directly at the center of the table, the directional vector matches the negative positional vector.

Other options that can be set in the config.yaml:

- Skip frames: Each video source can be set to skip a certain number of frames before starting the calculation. This can help with synchronisation of multiple cameras. Can be set to 0 for no delay.
- Factor: The pixel-to-centimeter ratio, has to be measured for every camera type. Place a ruler 10 cm in front of the camera lens and measure the distance of one centimeter in pixels (e.g. for the Raspberry Pi cameras, factor is 138)
- Resolution and FPS: Enter the picture resolution and FPS of the recordings here. Needed for ball tracking as well as speed calculation.
- Background Subtraction: This option can be used to filter background noise caused by non-moving objects in the orange colour spectrum, like walls for example. This will reduce performance, so deactivate it when not needed.
- Show images: Display the images while running the program. If set to true, this will show a window for each recording while doing the calculations. The recognized object is highlighted with blue borders.

After setting all needed and desired options in the config file, the program is ready to use. It will ask for a video file name. Enter the common name of the files you want to analyze and replace the number at the end with '{}'. After that, the script will run through the recordings and show the progress in the command line. In the current version it will then display the number of recognized hits and the maximum ball speed during the recording.

## Recording Manager for Raspberry Pi with Pi Camera
The recording manager can be used to create recordings for later analysis using the main program. It is specifically written for a setup with multiple Raspberry Pi's with attached Camera Modules. They have to be usable with the standard tools "rasivid" and "raspistill", these tools are included by default with Raspberry Pi OS.

#### Setup
To setup the recording manager it is necessary to enter the correct IP-Details into the file `recording-manager/peer-management.py` with the subnet and the offsets of the IP's belonging to the camera units.


After that the Repository code with the modified IP-Location can be transferred on all Camera Devices, for example using SSH Secure Copy (scp). Additionally some dependencies are necessary to be installed on each device. Namely a recent version (>=3.6) of Python and the package managing tool pipenv. On Raspberry Pi OS the dependencies can be ensure with the following command:

	sudo apt update && sudo apt install -y python3 pipenv

#### Usage

The recording manager consists of a simple Web-Application that can be started with executing the helper script:

	./start.sh

This starts a webserver at Port 5000, so you can access it at `http://1.2.3.4:5000` with a browser. `1.2.3.4` is the IP-Adress of a camera unit.

Using the webportal it is possible to select settings and start a parallel recording using all registered peers. For setting up the camera positions a preview image can be used where images from all nodes are displayed on one page. On page refresh new images are captured and displayed.