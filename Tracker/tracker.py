import pyrealsense2 as rs
import numpy as np
import cv2


pipeline = rs.pipeline() # declares and initializes the pipeline variable
config = rs.config() # declares and initializes the config variable for the pipeline
config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 30) # this starts the depth stream and sets the size and format
config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 30) # this starts the color stream and set the size and format
profile = pipeline.start(config)

# wait for five frames so that camera can autoexpose to lighting
# for x in range(5):
#   pipeline.wait_for_frames()
# print("Ready")

def getDist(depth_frame, bbox):

    # This creates a 9 by 9 grid of points within the given bounding box and stores each of the points distance in an array
    
    # bbox[x coordinate of the top left of the bounding box, y coordinate of the top left of the bounding box, width of box, height of box]
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
            distances = np.append(distances, depth_frame.get_distance(int(xTopLeft+currX), int(yTopLeft+currY)))
        currY = 0
    
    distances = np.sort(distances) # sorts the distances from least to greatest
    distances = distances[distances!=0.0] # removes all occurances of 0.0 (areas where there is not enough data return 0.0 as depth)
    median = np.median(distances) # gets the median from the array
    std = np.std(distances) # gets the standard deviation from th array
    # print("depth image median, std: ",median,std)
    modifiedDistances = [] # initializes a new array for removing outlier numbers

    # goes through distances array and adds any values that are less than X*standard deviations and ignores the rest
    for i in range(np.size(distances)):
        if abs(distances[i] - median) < 2.5 * std: # tune the standard deviation range for better results
            modifiedDistances = np.append(modifiedDistances,distances[i])

    # play around with what values give the most accurate distance
    modifiedDistances = np.sort(modifiedDistances)
    distance = (np.mean(modifiedDistances)+np.median(modifiedDistances))/2
    # distance = np.mean(modifiedDistances)
    # distance = np.median(modifiedDistances)
    print("depth frame first and last value",modifiedDistances[0], modifiedDistances[len(modifiedDistances)-1])
    print("The camera is facing an object ", distance, "meters away ")

def getDistFromArray(depth_frame_array, bbox):

    # This creates a 9 by 9 grid of points within the given bounding box and stores each of the points distance in an array
    
    # bbox[x coordinate of the top left of the bounding box, y coordinate of the top left of the bounding box, width of box, height of box]
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
    
    distances = np.sort(distances) # sorts the distances from least to greatest
    distances = distances[distances!=0.0] # removes all occurances of 0.0 (areas where there is not enough data return 0.0 as depth)
    median = np.median(distances) # gets the median from the array
    std = np.std(distances) # gets the standard deviation from th array

    modifiedDistances = [] # initializes a new array for removing outlier numbers

    # goes through distances array and adds any values that are less than X*standard deviations and ignores the rest
    for i in range(np.size(distances)):
        if abs(distances[i] - median) < 2.5 * std: # tune the standard deviation range for better results
            modifiedDistances = np.append(modifiedDistances,distances[i])

    # play around with what values give the most accurate distance
    modifiedDistances = np.sort(modifiedDistances)
    distance = (np.mean(modifiedDistances)+np.median(modifiedDistances))/2
    # distance = np.mean(modifiedDistances)
    # distance = np.median(modifiedDistances)
    print("array first and last ",modifiedDistances[0], modifiedDistances[len(modifiedDistances)-1])

    print("The camera is facing an object ", distance, "meters away ")


# this is the bounding box for testing in the format 
# bbox[x coordinate of the top left of the bounding box, y coordinate of the top left of the bounding box, width of box, height of box]

bbox = [410,140,65,120]
#bbox = [400,250,100,100]  
#bbox = [400,200,100,100]

depth_frames = []  
value = 0

try:
    while True:
        
        
        frames = pipeline.wait_for_frames() # gets all frames
        depth_frame = frames.get_depth_frame() # gets the depth frame
        color_frame = frames.get_color_frame() # gets the color frame 

        # we don't need this because we set the dimensions in the config before starting our pipeline
        # align_to = rs.stream.color
        # align = rs.align(align_to)
        # aligned_frames = align.process(frames) # aligns all the frames with the color frame
        # aligned_depth_frame = aligned_frames.get_depth_frame() # gets the new depth frame that is aligned
        # color_frame = aligned_frames.get_color_frame() # gets the color frame that the depth frame is aligned to
        

        # if there is no aligned_depth_frame or color_frame then leave the loop
        if not depth_frame or not color_frame:
            continue
        
        
        colorizer = rs.colorizer()
        # #DECIMATION FILTER
        # decimation = rs.decimation_filter()
        # # decimation.set_option(rs.option.filter_magnitude, 4)
        # decimated_depth = decimation.process(depth_frame)
        # decimated_image = np.asanyarray(decimated_depth.get_data())
        # colorized_depth = np.asanyarray(colorizer.colorize(decimated_depth).get_data())

        # SPATIAL FILTER
        spatial = rs.spatial_filter()
        spatial.set_option(rs.option.filter_magnitude, 5)
        spatial.set_option(rs.option.filter_smooth_alpha, 1)
        spatial.set_option(rs.option.filter_smooth_delta, 50)
        spatial.set_option(rs.option.holes_fill, 3)
        filtered_depth = spatial.process(depth_frame)
        filtered_image = np.asanyarray(filtered_depth.get_data())
        colorized_depth = np.asanyarray(colorizer.colorize(filtered_depth).get_data())

        # TEMPORAL FILTER
        # temporal = rs.temporal_filter()
        # depth_frames.append(frames.get_depth_frame())
        # for x in range(len(depth_frames)):
        #     temp_filtered = temporal.process(depth_frames[x])
        # filtered_image = np.asanyarray(temp_filtered.get_data())
        # colorized_depth = np.asanyarray(colorizer.colorize(temp_filtered).get_data())

        # HOLE FILLING FILTER
        # hole_filling = rs.hole_filling_filter()
        # filled_depth = hole_filling.process(depth_frame)
        # filtered_image = np.asanyarray(filled_depth.get_data())
        # colorized_depth = np.asanyarray(colorizer.colorize(filled_depth).get_data())

        # FILTERS TOGETHER     
        # depth_to_disparity = rs.disparity_transform(True)
        # disparity_to_depth = rs.disparity_transform(False)
        # for x in range(len(depth_frames)):
        #     frame = depth_frames[x]
        #     frame = decimation.process(frame)
        #     frame = depth_to_disparity.process(frame)
        #     frame = spatial.process(frame)
        #     frame = temporal.process(frame)
        #     frame = disparity_to_depth.process(frame)
        #     frame = hole_filling.process(frame)

        # colorized_depth = np.asanyarray(colorizer.colorize(frame).get_data())

        # we turn the depth and color frames into numpy arrays because we need to draw a rectangle and stack the two arrays
        depth_image = np.asanyarray(depth_frame.get_data()) # this takes the aligned depth frame and converts the data into a numpy array
        color_image = np.asanyarray(color_frame.get_data()) # this takes the aligned color frame and converts the data into a numpy array
        color_image = cv2.rectangle(color_image, (bbox[0],bbox[1]), (bbox[0]+bbox[2],bbox[1]+bbox[3]),(255, 0, 0), 5) # this draws a bounding box

        # we can use this to see where there is no data by greying out the color image pixels 
        # grey_color = 153
        # depth_image_3d = np.dstack((depth_image,depth_image,depth_image))
        # zero_removed = np.where((depth_image <= 0), grey_color, color_image)

        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha = 0.04), cv2.COLORMAP_JET) # this puts a color efffect on the depth frame
        images = np.hstack((color_image, depth_colormap)) # this stacks the color image and the depth image next to each other
        #images = colorized_depth
        filtered_colormap = cv2.applyColorMap(cv2.convertScaleAbs(filtered_image, alpha = 0.04), cv2.COLORMAP_JET)

        images = np.hstack((depth_colormap, filtered_colormap))
        cv2.namedWindow('Align Example', cv2.WINDOW_NORMAL)
        cv2.imshow('Align Example', images)
        key = cv2.waitKey(1)

       
        print("decimated image", len(filtered_image[0]),len(filtered_image))
        getDist(depth_frame, bbox) # this is a call to the method to get the distance
        #getDistFromArray(depth_image, bbox)
        getDistFromArray(filtered_image, bbox)
        value += 1 
        print(value)
        # if you press escape or q you can cancel the process
        print("press escape to cancel")
        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break

finally:
    pipeline.stop()

