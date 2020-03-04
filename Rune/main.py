import cv2
import numpy as np
import random as rng

# VideoCapture(0) for webcam, otherwise string of file name/loc
cap = cv2.VideoCapture('rune.mp4')

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # convert frame to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # choose colors to filter out / set threshold / will depend on testing/lighting/camera
    lower_blue = np.array([50,175,100])
    upper_blue = np.array([255,255,255])
    
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    res = cv2.bitwise_and(frame , frame, mask= mask)
    
    #set rng seed and threshold
    rng.seed(123);
    threshold = 175;
    
    #here is grayscale if desired, but using the more binary-esque mask is more accurate
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    #remove smaller connected components
    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(mask, connectivity=8)
    
    sizes = stats[1:, -1]; nb_components = nb_components - 1
    
    min_size = 750
    
    output2 = np.zeros((output.shape))
    for i in range(0, nb_components):
        if sizes[i] >= min_size:
            output2[output == i + 1] = 255
    
    mask2 = cv2.blur(output2, (1, 1))
    
    mask2copy = np.uint8(mask2)
    
    canny_out = cv2.Canny(mask2copy, threshold, threshold*2)
    
    contours, h = cv2.findContours(canny_out, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    minRect = [None]*len(contours)
    for i, c in enumerate(contours):
        minRect[i] = cv2.minAreaRect(c)
            
    drawing = np.zeros((canny_out.shape[0], canny_out.shape[1], 3), dtype=np.uint8)
    
    for i, c in enumerate(contours):
        color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
        # contour
        cv2.drawContours(drawing, contours, i, color)
        # rotated rectangle
        box = cv2.boxPoints(minRect[i])
        box = np.intp(box) #np.intp: Integer used for indexing (same as C ssize_t; normally either int32 or int64)
        cv2.drawContours(drawing, [box], 0, color)
    
    #output image with minimum rectangle contouring
    cv2.imshow('Contours', drawing)
    
    # convert frame to grayscale
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # take grayscale and convert to binary
    # cv2.threshhold(frame, threshhold to pass, color to change all passing pixels, what to change it to (binary pref))
    # retval, threshold = cv2.threshold(gray, 155, 255, cv2.THRESH_BINARY)

    # remove things that aren't ellipse-like
    # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    # finalFrame = cv2.morphologyEx(threshold, cv2.MORPH_TOPHAT, kernel)

    # Display the resulting frame
    #cv2.imshow('frame',finalFrame)
    cv2.imshow('frame', frame)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows() 