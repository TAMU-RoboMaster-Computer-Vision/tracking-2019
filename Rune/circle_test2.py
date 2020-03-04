import cv2
import numpy as np
import time
# VideoCapture(0) for webcam, otherwise string of file name/loc
cap = cv2.VideoCapture('rune2.mp4')

while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # convert frame to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # choose colors to filter out / set threshold / will depend on testing/lighting/camera
    #lower_blue = np.array([50, 175, 100])
    #upper_blue = np.array([255, 255, 255])
    lower_blue = np.array([100, 150, 0])
    upper_blue = np.array([140, 255, 255])

    mask_img = cv2.inRange(hsv, lower_blue, upper_blue)
    res = cv2.bitwise_and(frame, frame, mask=mask_img)

    thickness_half = 10
    x = np.arange(0, frame.shape[1])
    y = np.arange(0, frame.shape[0])
    arr = np.zeros((y.size, x.size))

    cx = int(frame.shape[1] / 2)
    cy = int(frame.shape[0] / 2)
    r = 100.

    # The two lines below could be merged, but I stored the mask
    # for code clarity.
    mask_raw = (x[np.newaxis, :] - cx) ** 2 + (y[:, np.newaxis] - cy) ** 2
    mask = (mask_raw <= (r + thickness_half) ** 2) & (mask_raw >= (r - thickness_half) ** 2)
    result_img = np.multiply(mask_img, mask)

    arr[mask] = 123.

    # Remove small connected components
    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(mask_img, connectivity=8)
    sizes = stats[1:, -1];
    nb_components = nb_components - 1

    min_size = 300

    img2 = np.zeros((output.shape))
    # for every component in the image, you keep it only if it's above min_size
    for i in range(0, nb_components):
        if sizes[i] >= min_size:
            img2[output == i + 1] = 255

    cv2.imshow('Binary',img2)
    cv2.imshow('circle',arr)
    cv2.imshow('result', result_img)
    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask_img)
    cv2.imshow('res', res)

    if cv2.waitKey(100) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()