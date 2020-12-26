import pyrealsense2 as rs
import numpy as np
import cv2


# pipeline = rs.pipeline()
# profile = pipeline.start()


pipeline = rs.pipeline() # declares and initializes the pipeline variable
config = rs.config() # declares and initializes the config variable for the pipeline
config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 30) # this starts the depth stream and sets the size and format
config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 30) # this starts the color stream and set the size and format
profile = pipeline.start(config)


try:
    while True:
        frames = pipeline.wait_for_frames()

        color_frame = frames.get_color_frame()
        cwidth = color_frame.get_width()
        cheight = color_frame.get_height()
        depth_frame = frames.get_depth_frame()
        dwidth = color_frame.get_width()
        dheight = color_frame.get_height()

        print(cwidth, cheight)
        print(dwidth, dheight)
finally:
    pipeline.stop()

