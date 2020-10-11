
    white = np.array([199,199,199])
    white2 = np.array([201,201,201])

    mask = cv2.inRange(frame, white, white2)
    contours,_ = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    boundingBoxes = []
    

    for contour in contours:        

        x,y,w,h = cv2.boundingRect(contour)
        cv2.rectangle(mask,(x,y),(x+w,y+h),(75,255,100),5)

        area = cv2.contourArea(contour)

        for boxIndex in range(len(boundingBoxes)):
            box = boundingBoxes[boxIndex]
            if (box[0]+box[2] >= x and x+w >= box[0]) and (box[1]+box[3] >= y and y+h >= box[1]) and area<box[4]*1.5:
                boundingBoxes.remove(box)
                break
    cv2.imshow('mask',mask)