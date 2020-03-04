import cv2
import numpy as np
import random as rng

#if needed
def sort_contours(cnts, method="left-to-right"):
	# initialize the reverse flag and sort index
	reverse = False
	i = 0
	# handle if we need to sort in reverse
	if method == "right-to-left" or method == "bottom-to-top":
		reverse = True
	# handle if we are sorting against the y-coordinate rather than
	# the x-coordinate of the bounding box
	if method == "top-to-bottom" or method == "bottom-to-top":
		i = 1
	# construct the list of bounding boxes and sort them from top to
	# bottom
	boundingBoxes = [cv2.boundingRect(c) for c in cnts]
	(cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
		key=lambda b:b[1][i], reverse=reverse))
	# return the list of sorted contours and bounding boxes
	return (cnts, boundingBoxes)

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
    
    # here is grayscale if desired, but using the more binary-esque mask is more accurate
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
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
    
    contours2 = []
    threshold_area = 2500
    threshold_area2 = 5000
    #filter out contour values based on certain criteria (just a frame, needs tweaking)
    for i in range(len(contours)):   
        bbox = cv2.boundingRect(contours[i])
        # rect = cv2.minAreaRect(contours[i])
        width = bbox[2]
        height = bbox[3]
        # use above if want to detect ratios
        area = width * height        
        if (area > threshold_area) and (area < threshold_area2):#check if area inside threshold   
            if(width / height < 1.5) and (width / height > 0.8):
                contours2.append(contours[i])
    contours = contours2
    
    #sort contours from largest to smallest, take however many values as needed
    contours = sorted(contours2, key=cv2.contourArea, reverse=True)[-1:]
            
    # if bounding boxes are needed
    '''
    cnts, bboxes = sort_contours(contours)
    
    bbox = min(bboxes)
    p1 = (int(bbox[0]), int(bbox[1]))
    p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
    #cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
    '''
    
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
    
    # output image with minimum rectangle contouring
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