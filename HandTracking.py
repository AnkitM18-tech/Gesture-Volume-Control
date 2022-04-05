import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

pTime = 0
cTime = 0

while True:
    success,img = cap.read()
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    # Checking if hands are detected
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id,lm in enumerate(handLms.landmark):
                # print(id,lm)
                h,w,c = img.shape
                cx,cy = int(lm.x * w), int(lm.y * h)
                # print(id,cx,cy)
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
    # FPS
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,f'FPS: {int(fps)}',(10,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),2)
    # Displaying the Frames
    cv2.imshow("Image",img)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break