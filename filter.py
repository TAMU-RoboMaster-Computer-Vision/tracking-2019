import cv2
import numpy as np
from math import sqrt,degrees,acos


cap = cv2.VideoCapture('rune.mp4')
counter = 0
MPx,MPy = 0,0
small_image = cv2.imread('mask_R.PNG')
ax,ay = 0,0

while(True):
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # convert from BGR to HSV

    # set lower and upper bound on color to only get blue and find the contours
    blueLight = np.array([40,170,100]) 
    blueDark = np.array([255,255,255])
    mask = cv2.inRange(hsv, blueLight, blueDark)
    contours,_ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    boundingBoxes = []

    # set lower and upper bound on color to only get arrows of current bounding box and find contours
    blueLight = np.array([0,75,150])
    blueDark = np.array([153,255,255])
    mask2 = cv2.inRange(hsv, blueLight, blueDark)
    contours2,_ = cv2.findContours(mask2,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

    # go through every small filttered contour and if it is within a certain size, set its x and y value to ax and ay which we will use to calculate angle later
    for contour in contours2:
        area = cv2.contourArea(contour)
        
        if area>15 and area<150:
            x,y,w,h = cv2.boundingRect(contour)
            ax,ay = x+w/2,y+h/2
            break

    # every 30 frames get the new position of the r image
    if counter%30 == 0:
        result = cv2.matchTemplate(small_image, frame, cv2.TM_SQDIFF_NORMED)
        mn,_,mnLoc,_ = cv2.minMaxLoc(result)
        MPx,MPy = mnLoc
    counter+=1

    for contour in contours:
        area = cv2.contourArea(contour)
        
        
        if area> 600: # filter contour based on minimum area
            x,y,w,h = cv2.boundingRect(contour)
            status = True

            # go through every box to make sure the current box doesn't overlap, if it does then find the one with the largest distance from the center and keep that one
            for boxIndex in range(len(boundingBoxes)):
                box = boundingBoxes[boxIndex]
                if (box[0]+box[2] >= x and x+w >= box[0]) and (box[1]+box[3] >= y and y+h >= box[1]):
                    height,width = frame.shape[:2]
                    cxBox = x+w/2
                    cyBox = y+h/2
                    cxDiff = MPx - cxBox
                    cyDiff = MPy - cyBox
                    distFromCenter = sqrt(cxDiff**2+cyDiff**2)
                    if distFromCenter>box[5]:
                        boundingBoxes.remove(box)
                        boundingBoxes.append([x,y,w,h,area,distFromCenter])
                    status = False
                    break
            if status:
                    height,width = frame.shape[:2]
                    cxBox = x+w/2
                    cyBox = y+h/2
                    cxDiff = MPx - cxBox
                    cyDiff = MPy - cyBox
                    distFromCenter = sqrt(cxDiff**2+cyDiff**2)
                    boundingBoxes.append([x,y,w,h,area,distFromCenter])

    # calculate average distance from center for the bounding boxes
    averageDistance = 0
    for box in boundingBoxes:
        averageDistance += box[5]
    if averageDistance!=0:
        averageDistance/=len(boundingBoxes)
        averageDistance*=.75

    # get rid of faulty boxes by checking if their distance is below average distance times a certain bias
    boxes = []
    for box in boundingBoxes:
        if box[5]>averageDistance:
            boxes.append(box)
    boundingBoxes=boxes

    # calculate the angle between every bounding box and the arrow with respect to the center using a dot b = |a||b|cos(theta) and set the bounding box to the one with the smallest angle
    bestBox,angle = None,360
    arrowToCenter=np.array([ax-MPx,ay-MPy])
    for box in boundingBoxes:
        boxToCenter = np.array([box[0]+1/2*box[2]-MPx,box[1]+1/2*box[3]-MPy])
        dotProduct = np.dot(arrowToCenter,boxToCenter)
        mag1 = sqrt(np.sum(arrowToCenter**2))
        mag2 = sqrt(np.sum(boxToCenter**2))
        angle2 =  degrees(acos(dotProduct/(mag1*mag2)))
        bestBox,angle = (bestBox,angle) if angle2>angle else (box,angle2)

    if bestBox:
        cv2.rectangle(frame,(bestBox[0],bestBox[1]),(bestBox[0]+bestBox[2],bestBox[1]+bestBox[3]),(0,255,0),5)

    cv2.imshow('frame',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break