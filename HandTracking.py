import cv2
import mediapipe as mp
import time

class HandDetector():
    def __init__(self, mode = False,maxHands = 2,modelComplexity = 1,detectionConf = 0.5,trackConf = 0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplexity = modelComplexity
        self.detectionConf = detectionConf
        self.trackConf = trackConf

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,self.modelComplexity,self.detectionConf,self.trackConf)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self,img,draw=True):
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # Checking if hands are detected
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img
        
        # Getting the landmark list
        # for id,lm in enumerate(handLms.landmark):
        #     # print(id,lm)
        #     h,w,c = img.shape
        #     cx,cy = int(lm.x * w), int(lm.y * h)
        #     # print(id,cx,cy)
                

def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    # Creating detector object
    detector = HandDetector()
    while True:
        success,img = cap.read()
        img = detector.findHands(img)
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

if __name__ == '__main__':
    main()