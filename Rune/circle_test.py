import numpy as np
import matplotlib.pyplot as plt
import cv2

frame=cv2.imread('test_img.png')
thickness_half=2
x = np.arange(0, frame.shape[1])
y = np.arange(0, frame.shape[0])
arr = np.zeros((y.size, x.size))

cx = int(frame.shape[1]/2)
cy = int(frame.shape[0]/2)
r = 100.

# The two lines below could be merged, but I stored the mask
# for code clarity.
mask_raw=(x[np.newaxis,:]-cx)**2 + (y[:,np.newaxis]-cy)**2
mask = (mask_raw <= (r + thickness_half) ** 2) & (mask_raw >= (r - thickness_half) ** 2)
arr[mask] = 123.
cv2.imshow('result',arr)
cv2.waitKey()
# This plot shows that only within the circle the value is set to 123.
# plt.figure(figsize=(6, 6))
# plt.pcolormesh(x, y, arr)
# plt.colorbar()
# plt.show()