# # Imports the MOSSE tracker from OpenCV
# from cv2 import TrackerMOSSE_create
# import pyrealsense2 as rs

# # Creates the MOSSE tracker object
# tracker = TrackerMOSSE_create()


# # Finds the absolute distance between two points
# def distance(point_1, point_2):
    
#     # Calculates the distance using Python spagettie
#     distance = (sum((p1 - p2) ** 2.0 for p1, p2 in zip(point_1, point_2))) ** (1 / 2)

#     # Returns the distance between two points
#     return distance

# def distBox(xTopLeft, yTopLeft, width, height):
#     try:
#         for i in range(0, 100):
#             frames = pipe.wait_for_frames()

#             for f in frames:
#                 depth = frames.get_depth_frame()
#                 # This creates an array of a 9 by 9 grid and stores each of the points distance in an array
#                 x_interval = width/10
#                 y_interval = height/10
#                 currX = 0
#                 currY = 0
#                 distances = []
#                 for i in range(10):
#                     currX += x_interval
#                     for j in range(10):
#                         currY += y_interval
#                         distances.append(depth.get_distance((xTopLeft+currX), (yTopLeft+currY)))
#                 distance = statistics.median(distances.sort())
#                 print("The camera is facing an object ", distance, "meters away ")
#     finally:
#         pipe.stop()

# # Starts tracking the object surrounded by the bounding box in the image
# # bbox is [x, y, width, height]
# def init(image, bboxes, video = []):
#     print("hllow")

#     # Finds the coordinate for the center of the screen
#     center = (image.shape[1] / 2, image.shape[0] / 2)

#     # Makes a dictionary of bounding boxes using the bounding box as the key and its distance from the center as the value 
#     bboxes = {bbox: distance(center, (bbox[0] + bbox[2] / 2, bbox[1] + bbox[3] / 2)) for bbox in bboxes}

#     # Finds the centermost bounding box
#     bbox = min(bboxes, key=bboxes.get)
	
# 	# Find the distance to the object
#     print(bbox)
	
	
#     # Attempts to start the tracker
#     ok = tracker.init(image, bbox)

#     # Checks if the initialization was successful
#     if ok:

#         # Goes through each frame that occurred since the first image was found
#         for frame in video:
#             ok = update(frame)

#     # Returns the tracker's status
#     return ok
# '''
# def init(frame, bboxes):
#     frame = cv2.imread(frame)
#     # Finds the coordinate for the center of the screen
#     center = (frame.shape[1] / 2, frame.shape[0] / 2)

#     # Makes a dictionary of bounding boxes using the bounding box as the key and its distance from the center as the value 
#     for i in bboxes:
#         x, y, width, height = i
        
#         center_bbox = x + width / 2, y + height / 2
        
#         cv2.imshow("Tracking", frame)
    

#     #bboxes_dict = {bbox: distance(center, (center_bbox)) for bbox in bboxes}
    
#     bboxes_dict = {}
    
#     for i in bboxes:
#         i = tuple(i)
#         bboxes_dict = {i: distance(center, (center_bbox))}
        
#     # Finds the centermost bounding box
#     bbox = (0, 0, 0, 0)
#     minimum = 999999
#     for i in bboxes_dict:
#         if bboxes_dict[i] < minimum:
#             minimum = bboxes_dict[i]
#             bbox = i
#     print(minimum)
#     print(bbox)
    
    
    
#     p1 = (int(bbox[0]), int(bbox[1]))
#     p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
#     cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
    
#     cv2.imshow("Tracking", frame)
# '''
    
    

# # Updates the location of the object
# def update(image):

#     # Attempts to update the object's location
#     ok, location = tracker.update(image)

#     # Returns the location if the location was updated
#     if ok:
#         # return location
#         return (location[0] + location[2] / 2, location[1] + location[3] / 2)

#     # Returns false the updating the location fails
#     else:
#         return False
    
    
# bboxes = [[22, 20, 46, 60], [2222, 522, 32, 92], [90, 333, 111, 44]]
# import cv2
# import numpy as np
# print("Environment Ready")
# # Creates Pipe
# pipe = rs.pipeline()
# cfg = rs.config()
# cfg.enable_stream(rs.stream.depth,1280,720,rs.format.z16,30)
# cfg.enable_stream(rs.stream.color,1280,720,rs.format.bgr8,30)
# profile = pipe.start(cfg)
# align=rs.align(rs.stream.color)

# frames = pipe.wait_for_frames()
# depth_frame = frames.get_depth_frame()
# aligned_frames=align.process(frames)

# frame=aligned_frames.get_color_frame()
# frame=np.asanyarray(frame.get_data())
# bbox = cv2.selectROI(frame, False)


# init(frame, [bbox])
# # frame = 

# import pyrealsense2 as rs
# import cv2

# pipeline = rs.pipeline()
# pipeline.start()

# # Streaming loop
# try:
#     while True:
#        frames = pipeline.wait_for_frames()
    #    depth_frame = frames.get_depth_frame()
    #    if not depth_frame: continue
    #    width = depth_frame.get_width()
    #    height = depth_frame.get_height()
#        #print(width,height)
        
#        #Calculate distance
#        dist_to_center = depth_frame.get_distance(int(width/2), int(height/2))
#        print('The camera is facing an object:',dist_to_center,'meters away')

# finally:
#     pipeline.stop()

# import numpy as np
# import matplotlib.pyplot as plt
# import pyrealsense2 as rs
# print("Environment Ready")

# pipe = rs.pipeline()
# profile = pipe.start()

# for x in range(5):
#     pipe.wait_for_frames()

# frameset = pipe.wait_for_frames()
# depth_frame = frameset.get_depth_frame()

# pipe.stop()
# print("Frames Captured")

# colorizer = rs.colorizer()
# colorized_depth = np.asanyarray(colorizer.colorize(depth_frame).get_data())

# plt.rcParams["axes.grid"] = False
# plt.rcParams['figure.figsize'] = [8,4]
# plt.imshow(colorized_depth)


import pyrealsense2 as rs
import numpy as np
import cv2


pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 30)
profile = pipeline.start(config)
for x in range(5):
  pipeline.wait_for_frames()
print("Ready")

depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()
print("Depth Scale is: " , depth_scale)

align_to = rs.stream.color
align = rs.align(align_to)

def getDist(depth_frame, bbox):
    # This creates an array of a 9 by 9 grid and stores each of the points distance in an array
    xTopLeft = bbox[0]
    yTopLeft = bbox[1]
    width = bbox[2]
    height = bbox[3]
    x_interval = width/10
    y_interval = height/10
    currX = 0
    currY = 0
    distances = np.array([])
    for i in range(10):
        currX += x_interval
        for j in range(10):
            currY += y_interval
            distances = np.append(distances, depth_frame.get_distance(int(xTopLeft+currX), int(yTopLeft+currY)))
        currY = 0
    distances = np.sort(distances)
    distances = distances[distances!=0.0]
    median = np.median(distances)
    std = np.std(distances)
    modifiedDistances = []

    for i in range(np.size(distances)):
        if abs(distances[i] - median) < 2.5 * std:
            modifiedDistances = np.append(modifiedDistances,distances[i])

    distance = (np.mean(modifiedDistances)+np.median(modifiedDistances))/2

    print("The camera is facing an object ", distance, "meters away ")


 
bbox = [405,210,75,90]
#bbox = [400,250,100,100]  
#bbox = [400,200,100,100          
try:
    while True:
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        aligned_frames = align.process(frames)

        aligned_depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()

        if not aligned_depth_frame or not color_frame:
            continue

        depth_image = np.asanyarray(aligned_depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        color_image = cv2.rectangle(color_image, (bbox[0],bbox[1]), (bbox[0]+bbox[2],bbox[1]+bbox[3]),(255, 0, 0), 5)


        grey_color = 153
        depth_image_3d = np.dstack((depth_image,depth_image,depth_image))
        zero_removed = np.where((depth_image_3d <= 0), grey_color, color_image)

        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha = 0.03), cv2.COLORMAP_JET)
        images = np.hstack((color_image, depth_colormap))
        cv2.namedWindow('Align Example', cv2.WINDOW_NORMAL)
        cv2.imshow('Align Example', images)
        key = cv2.waitKey(1)

       
        
        getDist(depth_frame, bbox)
        
        #print('The camera is facing an object:',dist_to_center,'meters away')
        print("press escape to cancel")
        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break
finally:
    pipeline.stop()

