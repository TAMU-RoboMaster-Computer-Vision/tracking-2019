from sys import exit as sys_exit
from time import time

from cv2 import TrackerMOSSE_create, VideoCapture, selectROI

# Creates the MOSSE tracker
tracker = TrackerMOSSE_create()

# Starts the camera stream
camera = VideoCapture('SOT/RoboMaster.mp4')

# Exits the program if the camera stream cannot be established
if not camera.isOpened():
    sys_exit()

# Gets the first frame from the camera
ok, current_frame = camera.read()

# Exits the program if the first frame cannot be pulled from the camera stream
if not ok:
    sys_exit()

# Gets the target location
target = selectROI(current_frame, False)

# Initializes the tracker
ok = tracker.init(current_frame, target)

# Exits the program if the tracker could not be initialized
if not ok:
    sys_exit()

# The number of frames that
history_length = 3

# Stores the targets location history
history_target = [[0, 0, 0]] * history_length

# Iterator used to keep track of how many times
i = 1

# The initial value for start time
time_start = time()

# Continues to track target until the camera stream is closed
while True:

    # Gets the next frame from the camera
    ok, frame_current = camera.read()

    # Exits the loop if the next frame could not be found
    if not ok:
        break

    # Updates the location of the target
    ok, target = tracker.update(frame_current)

    # Updates the target history list
    if ok:

        # Stores the x, y, and delta t (ms) of the last n frames
        history_target.append(list(target[:2] + ((time() - time_start) * 10 ** 6,)))
        time_start = time()

        # Removes the oldest frame
        history_target.pop(0)

        # Sets the time difference of the first time to zero
        history_target[0][2] = 0

    # Target is lost
    else:
        history_target = [[0, 0, 0]] * history_length
        break
    
    # Only prints new lists of data
    if i % history_length == 0:
        print(history_target)

    # Increments the iterator
    i += 1

print('Tracker was closed')