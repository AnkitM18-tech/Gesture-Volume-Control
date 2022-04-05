import cv2
import numpy as np
import time

# Dimensions
wCam,hCam = 640,480
pTime = 0

# Checking Webcam
cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

# Running loop to capture input from webcam
while True:
    success, img = cap.read()
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