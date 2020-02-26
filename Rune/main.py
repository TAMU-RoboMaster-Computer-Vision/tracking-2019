import cv2
import numpy as np

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