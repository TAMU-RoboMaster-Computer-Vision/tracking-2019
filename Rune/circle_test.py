import numpy as np
import matplotlib.pyplot as plt
import cv2

frame=cv2.imread('test_img.png')

# convert frame to HSV
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# choose colors to filter out / set threshold / will depend on testing/lighting/camera
lower_blue = np.array([50, 175, 100])
upper_blue = np.array([255, 255, 255])
mask_img = cv2.inRange(hsv, lower_blue, upper_blue)
res = cv2.bitwise_and(frame, frame, mask=mask_img)


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
result_img=np.multiply(mask_img,mask)

arr[mask] = 123.
cv2.imshow('result',result_img)
cv2.waitKey()
# This plot shows that only within the circle the value is set to 123.
# plt.figure(figsize=(6, 6))
# plt.pcolormesh(x, y, arr)
# plt.colorbar()
# plt.show()