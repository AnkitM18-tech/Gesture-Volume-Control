import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8,maxHands=2)

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img) #Draw method
    # hands = detector.findHands(img,draw=False) #No draw Method
    if hands:
        # Hand-1
        hand1 = hands[0]
        lmList1 = hand1["lmList"] #list of 21 landmark points
        bbox1 = hand1["bbox"] #bounding box information x,y,w,h
        centerPoint1 = hand1["center"] #center of hand cx,cy
        handType1 = hand1["type"] #hand Type Left or Right
        fingers1 = detector.fingersUp(hand1)
        # print(len(lmList1),lmList1)
        # print(bbox1)
        # print(centerPoint1)
        # print(handType1)
        # print(lmList1[8])
        # length,info,img = detector.findDistance(lmList1[8][:2],lmList1[12][:2],img) #draw image
        # length,info = detector.findDistance(lmList1[8][:2],lmList1[12][:2]) # no draw image

        if len(hands) == 2:
            hand2 = hands[1]
            lmList2 = hand2["lmList"] #list of 21 landmark points
            bbox2 = hand2["bbox"] #bounding box information x,y,w,h
            centerPoint2 = hand2["center"] #center of hand cx,cy
            handType2 = hand2["type"] #hand Type Left or Right
            fingers2 = detector.fingersUp(hand2)
            # print(len(lmList1),lmList1)
            # print(bbox1)
            # print(centerPoint1)
            # print(handType1)
            # print(fingers1,fingers2)
            length,info,img = detector.findDistance(lmList1[8][:2],lmList2[8][:2],img)
            length,info,img = detector.findDistance(centerPoint1,centerPoint2,img)

    cv2.imshow("Image",img)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break