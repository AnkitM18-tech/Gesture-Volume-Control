import cv2
import numpy as np
import time
import HandTracking as ht
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Dimensions
wCam,hCam = 640,480
pTime = 0

# Create detector object
detector = ht.HandDetector(detectionConf=0.8,maxHands=1)

# audio handling
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
# print(volume.GetMasterVolumeLevel())
# print(volume.GetVolumeRange()) #(-65.25,0.0,0.03125)
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volPercentage = 0
volBar = 400
area = 0
volColor = (255,0,0)

# Checking Webcam
cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

# Running loop to capture input from webcam
while True:
    success, img = cap.read()
    # detect hands
    img = detector.findHands(img)
    # getting the landmark list
    lmList,bbox = detector.findPosition(img, draw=True)
    if len(lmList) != 0:
        # Filter based on size
        area = ((bbox[2]-bbox[0]) * (bbox[3]-bbox[1])) // 100
        # print(bbox)
        # print(area)
        if 350 < area < 1000:
            # Find distance between Index and thumb
            length,img,lineInfo = detector.findDistance(4,8,img)

            # Convert Volume
            # vol = np.interp(length,[10,200],[minVol,maxVol])
            volBar = np.interp(length,[10,200],[400,150])
            volPercentage = np.interp(length,[10,200],[0,100])
            # print(int(length), vol)
            # volume.SetMasterVolumeLevel(vol, None)

            # Reduce resolution to make it smoother
            smoothness = 10
            volPercentage = math.ceil(smoothness * round(volPercentage/smoothness))
            # print(volPercentage)
            # Check fingers Up
            fingers = detector.fingersUp()
            # print(fingers)

            # if pinky finger is down, set volume
            if not fingers[4]:
                volume.SetMasterVolumeLevelScalar(volPercentage/100,None)
                cv2.circle(img, (lineInfo[4],lineInfo[5]), 5, (255,0,0),cv2.FILLED)
                volColor = (0,255,0)
                print(volPercentage)
                time.sleep(0.25)
            else:
                volColor = (255,0,0)
            
            # print(lmList[4],lmList[8])
            # x1, y1 = lmList[4][1], lmList[4][2]
            # x2, y2 = lmList[8][1], lmList[8][2]
            # cx, cy = (x1+x2)//2 , (y1+y2)//2
            # # marking the gesture fingers
            # cv2.circle(img,(x1,y1),5,(255,255,0),cv2.FILLED)
            # cv2.circle(img,(x2,y2),5,(255,255,0),cv2.FILLED)
            # cv2.line(img,(x1,y1),(x2,y2),(255,255,0),3)
            # cv2.circle(img,(cx,cy),5,(255,255,0),cv2.FILLED)
            # # finding the length of the connecting line
            # length = math.hypot(x2-x1,y2-y1)
            # print(length)
            # Hand Range 10 - 208
            # Volume Range -65 - 0
            # if length < 20:
            #     cv2.circle(img, (lineInfo[4],lineInfo[5]), 5, (255,0,0),cv2.FILLED)
    # Draw
    # Volume Bar
    cVol = int(volume.GetMasterVolumeLevelScalar()*100)
    cv2.rectangle(img, (50,150), (85,400),(255,0,0),3)
    cv2.rectangle(img, (50,int(volBar)), (85,400),(255,0,0),cv2.FILLED)
    cv2.putText(img,f"{volPercentage} %",(40,450), cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)
    cv2.putText(img,f"Vol Set: {int(cVol)}",(400,50), cv2.FONT_HERSHEY_COMPLEX,1,volColor,3)
    # fps
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    # showing fps value on the image
    cv2.putText(img,f"FPS: {int(fps)}",(40,50), cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)
    cv2.imshow("Image",img)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

# ?Previous Code

# import cv2
# import time
# import numpy as np
# import HandTrackingModule as htm
# import math
# from ctypes import cast, POINTER
# from comtypes import CLSCTX_ALL
# from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# ################################
# wCam, hCam = 640, 480
# ################################

# cap = cv2.VideoCapture(1)
# cap.set(3, wCam)
# cap.set(4, hCam)
# pTime = 0

# detector = htm.handDetector(detectionCon=0.7)

# devices = AudioUtilities.GetSpeakers()
# interface = devices.Activate(
#     IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
# volume = cast(interface, POINTER(IAudioEndpointVolume))
# # volume.GetMute()
# # volume.GetMasterVolumeLevel()
# volRange = volume.GetVolumeRange()
# minVol = volRange[0]
# maxVol = volRange[1]
# vol = 0
# volBar = 400
# volPer = 0
# while True:
#     success, img = cap.read()
#     img = detector.findHands(img)
#     lmList = detector.findPosition(img, draw=False)
#     if len(lmList) != 0:
#         # print(lmList[4], lmList[8])

#         x1, y1 = lmList[4][1], lmList[4][2]
#         x2, y2 = lmList[8][1], lmList[8][2]
#         cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

#         cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
#         cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
#         cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
#         cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

#         length = math.hypot(x2 - x1, y2 - y1)
#         # print(length)

#         # Hand range 50 - 300
#         # Volume Range -65 - 0

#         vol = np.interp(length, [50, 300], [minVol, maxVol])
#         volBar = np.interp(length, [50, 300], [400, 150])
#         volPer = np.interp(length, [50, 300], [0, 150])
#         print(int(length), vol)
#         volume.SetMasterVolumeLevel(vol, None)

#         if length < 50:
#             cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

#     cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
#     cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
#     cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX,
#                 1, (255, 0, 0), 3)


#     cTime = time.time()
#     fps = 1 / (cTime - pTime)
#     pTime = cTime
#     cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
#                 1, (255, 0, 0), 3)

#     cv2.imshow("Img", img)
#     cv2.waitKey(1)