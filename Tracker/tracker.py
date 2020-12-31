import pyrealsense2 as rs
import numpy as np
import cv2

from time import *
import threading

def countdown():
    global my_timer

    my_timer = 10

    for x in range(10):
        my_timer = my_timer - 1
        sleep(1)

    print("Out of time")


# pipeline = rs.pipeline()                                             # declares and initializes the pipeline variable
# pipeline.start()

pipeline = rs.pipeline()                                            # declares and initializes the pipeline variable
config = rs.config()                                                # declares and initializes the config variable for the pipeline
config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 60)  # this starts the depth stream and sets the size and format
config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 60) # this starts the color stream and set the size and format
profile = pipeline.start(config)


# This creates a 9 by 9 grid of points within the given bounding box and stores each of the points distance in an array
def getDistFromArray(depth_frame_array, bbox):
    
    xTopLeft = bbox[0] 
    yTopLeft = bbox[1]
    width = bbox[2]
    height = bbox[3]
    # this is used to add to the currentX and currentY so that we can get the different points in the 9x9 grid
    x_interval = width/10
    y_interval = height/10
    # stores the x and y of the last point in the grid we got the distance from
    currX = 0
    currY = 0
    distances = np.array([]) # empty numpy array to store 81 distances (9x9 grid)
    
    # double for loop to go through 2D array of 9x9 grid
    for i in range(10):
        currX += x_interval # add the interval you calculated to traverse through the 9x9 grid
        for j in range(10):
            currY += y_interval # add the interval you calculated to traverse through the 9x9 grid
            # gets the distance of the point from the depth frame on the grid and appends to the array
            distances = np.append(distances, depth_frame_array[int(yTopLeft+currY)][int(xTopLeft+currX)]/1000)
        currY = 0
    
    distances = np.sort(distances)          # sorts the distances from least to greatest
    distances = distances[distances!=0.0]   # removes all occurances of 0.0 (areas where there is not enough data return 0.0 as depth)
    median = np.median(distances)           # gets the median from the array
    std = np.std(distances)                 # gets the standard deviation from th array
    modifiedDistances = []                  # initializes a new array for removing outlier numbers

    # goes through distances array and adds any values that are less than X*standard deviations and ignores the rest
    for i in range(np.size(distances)):
        if abs(distances[i] - median) < 1.5 * std: # tune the standard deviation range for better results
            modifiedDistances = np.append(modifiedDistances,distances[i])

    modifiedDistances = np.sort(modifiedDistances)
    distance = (np.mean(modifiedDistances)+np.median(modifiedDistances))/2
    # distance = np.mean(modifiedDistances)
    # distance = np.median(modifiedDistances)
    print("array first and last ",modifiedDistances[0], modifiedDistances[len(modifiedDistances)-1])
    print("The camera is facing an object ", distance, "meters away ")


# bbox[x coordinate of the top left of the bounding box, y coordinate of the top left of the bounding box, width of box, height of box]
bbox = [410,140,65,120] # this is the bounding box for testing in the format 
value = 0
try:
    countdown_thread = threading.Thread(target = countdown)
    countdown_thread.start()
    while True and my_timer > 0:

        frames = pipeline.wait_for_frames()     # gets all frames
        depth_frame = frames.get_depth_frame()  # gets the depth frame
        color_frame = frames.get_color_frame()  # gets the color frame 
        if not depth_frame or not color_frame:  # if there is no aligned_depth_frame or color_frame then leave the loop
            continue

        # we turn the depth and color frames into numpy arrays because we need to draw a rectangle and stack the two arrays
        # depth_image = np.asanyarray(depth_frame.get_data()) # this takes the aligned depth frame and converts the data into a numpy array
        # depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha = 0.04), cv2.COLORMAP_JET)# this puts a color efffect on the depth frame
        # color_image = np.asanyarray(color_frame.get_data()) # this takes the aligned color frame and converts the data into a numpy array
        # color_image = cv2.rectangle(color_image, (bbox[0],bbox[1]), (bbox[0]+bbox[2],bbox[1]+bbox[3]),(255, 0, 0), 5) # this draws a bounding box to the color frame

        # SPATIAL FILTER
        # colorizer = rs.colorizer()
        # spatial = rs.spatial_filter()
        # spatial.set_option(rs.option.filter_magnitude, 1) # values 1-5 for intensity
        # spatial.set_option(rs.option.filter_smooth_alpha, 1) # values .25-1 for intensity
        # spatial.set_option(rs.option.filter_smooth_delta, 50) # values 1-50 for intensity
        # spatial.set_option(rs.option.holes_fill, 1) # values 1-5 for intensity
        # filtered_depth = spatial.process(depth_frame)
        # filtered_image = np.asanyarray(filtered_depth.get_data())
        # colorized_depth = np.asanyarray(colorizer.colorize(filtered_depth).get_data())
        # filtered_colormap = cv2.applyColorMap(cv2.convertScaleAbs(filtered_image, alpha = 0.04), cv2.COLORMAP_JET)  # this puts a color effect on the filtered depth frame
        
        # you can show: color_image, depth_colormap, filtered_colormap, colorized_depth
        # images = np.hstack((color_image, depth_colormap))     # use this if you want to compare streams
        # images = depth_colormap                              # use this for individual streams
        # cv2.namedWindow('Align Example', cv2.WINDOW_NORMAL)   # names and shows the streams
        # cv2.imshow('Align Example', images)
        # # if you press escape or q you can cancel the process
        # key = cv2.waitKey(1)
        # print("press escape to cancel")
        # if key & 0xFF == ord('q') or key == 27:
        #     cv2.destroyAllWindows()
        #     break

        # getDistFromArray(depth_image, bbox)     # gets the distance for the normal depth image
        # getDistFromArray(filtered_image, bbox)  # gets the distance for the filtered depth image
        value += 1 
        print(value)


finally:
    pipeline.stop()

