import cv2
import time
import os
import HandTracking as ht

# Dimensions
wCam, hCam = 640,480

# Settin up the Web Cam
cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

# Path of Images and Other Variables
folderPath = "Images"
pTime = 0
imgList = os.listdir(folderPath)
# print(imgList)
overLayList = []
for imPath in imgList:
    image = cv2.imread(f"{folderPath}/{imPath}")
    # print(f"{folderPath}/{imPath}")
    overLayList.append(image)

# print(len(overLayList))
# Creating Detector Object
detector = ht.HandDetector(detectionConf=0.8)

# tipIDS
tipIDs = [4,8,12,16,20]

# Capturing Frames and Displaying
while True:
    success,img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img,draw=False)
    # print(lmList)
    if len(lmList) != 0:
        fingers = []
        # Thumb
        if lmList[tipIDs[0]][1] > lmList[tipIDs[0]-1][1]:
            # print("Finger Open")
            fingers.append(1)
        else:
            fingers.append(0)
        # Fingers except Thumb
        for id in range(1,5):
            if lmList[tipIDs[id]][2] < lmList[tipIDs[id]-2][2]:
                # print("Finger Open")
                fingers.append(1)
            else:
                fingers.append(0)
        # print(fingers)
        totalFingers = fingers.count(1)
        # print(totalFingers)
        # Overlaying the image over our captured image 
        h,w,c = overLayList[totalFingers-1].shape
        img[0:h,0:w] = overLayList[totalFingers-1]
        # Showing count in rectangle
        cv2.rectangle(img,(20,300),(170,465),(0,255,0),cv2.FILLED)
        cv2.putText(img,str(totalFingers),(45,440),cv2.FONT_HERSHEY_PLAIN,10,(255,0,0),20)
    # FPS
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, f"FPS: {int(fps)}",(400,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    cv2.imshow("Image",img)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break