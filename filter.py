import cv2
import numpy as np
from math import sqrt,degrees,acos

# DO ANGLE BETWEEN VECTORS FOR LIGHT BLUE STICK ONCE HIT

cap = cv2.VideoCapture('rune.mp4')
counter = 0
MPx,MPy = 0,0
small_image = cv2.imread('mask_R.PNG')
ax,ay = 0,0
# arrow = cv2.imread('arrow.PNG')
while(True):
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    blueLight = np.array([40,170,100])
    blueDark = np.array([255,255,255])
    mask = cv2.inRange(hsv, blueLight, blueDark)
    contours,_ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    boundingBoxes = []

    # if counter%5 == 0:
    #     result = cv2.matchTemplate(arrow, frame, cv2.TM_SQDIFF_NORMED)
    #     mn,_,mnLoc,_ = cv2.minMaxLoc(result)
    #     ax,ay = mnLoc
    #     print(ax)
    #     print(ay)2
    blueLight = np.array([0,75,150])
    blueDark = np.array([153,255,255])
    mask2 = cv2.inRange(hsv, blueLight, blueDark)
    contours2,_ = cv2.findContours(mask2,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    print(len(contours2))
    for contour in contours2:
        area = cv2.contourArea(contour)
        
        if area>30 and area<100:
            x,y,w,h = cv2.boundingRect(contour)
            ax,ay = x+w/2,y+h/2


    if counter%30 == 0:
        result = cv2.matchTemplate(small_image, frame, cv2.TM_SQDIFF_NORMED)
        mn,_,mnLoc,_ = cv2.minMaxLoc(result)
        MPx,MPy = mnLoc
    counter+=1

    for contour in contours:
        area = cv2.contourArea(contour)
        
        if area> 800:
            cv2.drawContours(frame,contour,-1,(200,200,200),2)
            x,y,w,h = cv2.boundingRect(contour)
            status = True

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

    # white = np.array([199,199,199])
    # white2 = np.array([201,201,201])

    # mask = cv2.inRange(frame, white, white2)
    # contours,_ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    # boundingBoxes = []
    

    # for contour in contours:        

    #     x,y,w,h = cv2.boundingRect(contour)
    #     cv2.rectangle(mask,(x,y),(x+w,y+h),(75,255,100),5)

    #     area = cv2.contourArea(contour)

    #     for boxIndex in range(len(boundingBoxes)):
    #         box = boundingBoxes[boxIndex]
    #         if (box[0]+box[2] >= x and x+w >= box[0]) and (box[1]+box[3] >= y and y+h >= box[1]) and area<box[4]*1.5:
    #             boundingBoxes.remove(box)
    #             break
    # cv2.imshow('mask',mask)

    bestBox,angle = None,360
    arrowToCenter=np.array([ax-MPx,ay-MPy])
    for box in boundingBoxes:
        boxToCenter = np.array([box[0]+1/2*box[2]-MPx,box[1]+1/2*box[3]-MPy])

        dotProduct = np.dot(arrowToCenter,boxToCenter)
        mag1 = sqrt(np.sum(arrowToCenter**2))
        mag2 = sqrt(np.sum(boxToCenter**2))
        angle2 =  degrees(acos(dotProduct/(mag1*mag2)))
        bestBox,angle = (bestBox,angle) if angle2>angle else (box,angle2)

    # for box in boundingBoxes:
    #     if box[5]>=averageDistance:
    #         cv2.rectangle(frame,(box[0],box[1]),(box[0]+box[2],box[1]+box[3]),(0,255,0),5)
    cv2.rectangle(frame,(bestBox[0],bestBox[1]),(bestBox[0]+bestBox[2],bestBox[1]+bestBox[3]),(0,255,0),5)

        # make sure bbox dont overlap and if they do, take the smallest one
        # convert to polar, take average distance, take all the ones above average distance


    # cv2.imshow('mask',mask)
    cv2.imshow('frame',frame)


    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break