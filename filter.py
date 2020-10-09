import cv2
import numpy as np
from math import sqrt

# CALCULATE CENTER WITH IMAGE OF R
# CALCULATE H AND W MAX WITH DISTANCE FROM TARGET MODEL USING INTEL API

cap = cv2.VideoCapture('rune.mp4')
counter = 0
MPx,MPy = 0,0
small_image = cv2.imread('mask_R.PNG')
while(True):
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    blueLight = np.array([40,170,100])
    blueDark = np.array([255,255,255])
    mask = cv2.inRange(hsv, blueLight, blueDark)
    contours,_ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    boundingBoxes = []


    if counter%30 == 0:
        result = cv2.matchTemplate(small_image, frame, cv2.TM_SQDIFF_NORMED)
        mn,_,mnLoc,_ = cv2.minMaxLoc(result)
        MPx,MPy = mnLoc
    counter+=1
    
    for contour in contours:
        area = cv2.contourArea(contour)
        
        if area> 800:
            cv2.drawContours(frame,contour,-1,(255,255,255),2)
            x,y,w,h = cv2.boundingRect(contour)
            status = True
            # if h>70 or w>70:
            #     continue
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

    averageDistance = 0
    for box in boundingBoxes:
        averageDistance += box[5]
    if averageDistance!=0:
        averageDistance/=len(boundingBoxes)
        averageDistance*=.65

    for box in boundingBoxes:
        if box[5]>=averageDistance:
            cv2.rectangle(frame,(box[0],box[1]),(box[0]+box[2],box[1]+box[3]),(0,255,0),5)
    
        # make sure bbox dont overlap and if they do, take the smallest one
        # convert to polar, take average distance, take all the ones above average distance


    # cv2.imshow('mask',mask)
    cv2.imshow('frame',frame)


    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break