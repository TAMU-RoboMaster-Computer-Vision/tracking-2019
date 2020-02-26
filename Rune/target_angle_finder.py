import cv2
import numpy as np
class target_angle_finder:
    def __init__(self,img_w,img_h,radius_gap=6,thickness_half=2):
        self.thickness_half=thickness_half
        self.img_w=img_w
        self.img_h=img_h
        self.radius_gap=radius_gap

    def init_mask(self):
        x = np.arange(0, self.img_w)
        y = np.arange(0, self.img_h)
        arr = np.zeros((y.size, x.size))
        cx = int(x / 2)
        cy = int(y / 2)
