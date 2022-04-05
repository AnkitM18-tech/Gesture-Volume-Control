from tokenize import detect_encoding
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
detector = ht.HandDetector(detectionConf=0.8)

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
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        # print(lmList[4],lmList[8])
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1+x2)//2 , (y1+y2)//2
        # marking the gesture fingers
        cv2.circle(img,(x1,y1),5,(255,255,0),cv2.FILLED)
        cv2.circle(img,(x2,y2),5,(255,255,0),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,255,0),3)
        cv2.circle(img,(cx,cy),5,(255,255,0),cv2.FILLED)
        # finding the length of the connecting line
        length = math.hypot(x2-x1,y2-y1)
        # print(length)
        # Hand Range 10 - 208
        # Volume Range -65 - 0
        vol = np.interp(length,[10,210],[minVol,maxVol])
        volBar = np.interp(length,[10,210],[400,150])
        volPercentage = np.interp(length,[10,210],[0,100])
        # print(int(length), vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length < 20:
            cv2.circle(img, (cx,cy), 5, (255,0,0),cv2.FILLED)
    # Volume Bar
    cv2.rectangle(img, (50,150), (85,400),(255,0,0),3)
    cv2.rectangle(img, (50,int(volBar)), (85,400),(255,0,0),cv2.FILLED)
    cv2.putText(img,f"{int(volPercentage)} %",(40,450), cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),3)
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