import cv2
def movement_detection(img_last,img_now):
    img_last_gray=cv2.cvtColor(img_last, cv2.COLOR_BGR2GRAY)
    img_now_gray=cv2.cvtColor(img_now, cv2.COLOR_BGR2GRAY)

    diff=cv2.absdiff(img_last_gray,img_now_gray)
    diff_thresh=cv2.threshold(diff,75,255,cv2.THRESH_BINARY)[1]

    diff_thresh = cv2.dilate(diff_thresh, None, iterations=0)
    #kernel_erode=cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
    #kernel_dilate=cv2.getStructuringElement(cv2.MORPH_RECT,(15,15))

    #cv2.erode(diff_thresh,kernel_erode,1)
    #cv2.dilate(diff_thresh,kernel_dilate,1)

    contours,_=cv2.findContours(diff_thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    res=img_now.copy()

    bounding_boxes = [cv2.boundingRect(cnt) for cnt in contours]
    for bbox in bounding_boxes:
        [x , y, w, h] = bbox
        cv2.rectangle(res, (x, y), (x + w, y + h), (0, 255, 0), 2)

    #cv2.imwrite("test.jpg",res)
    #cv2.imshow("test",res)
    
    print("contours.size=",len(contours))
    return len(contours),res
