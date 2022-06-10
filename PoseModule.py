import cv2
import mediapipe as mp
import time
import argparse
import sys
sys.path.append(".\controller")
import UdpComms as U

# parser = argparse.ArgumentParser(description='Pose detection script for freeride game')
# parser.add_argument('--debug', action='store_true')
# args = vars(parser.parse_args())

sock = U.UdpComms(udpIP="127.0.0.1", portTX=8001, portRX=8003, enableRX=True, suppressWarnings=True)

class PoseDetector:

    def __init__(self, mode = False, upBody = False, smooth=True, detectionCon = 0.5, trackCon = 0.5):

        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.upBody, self.smooth, self.detectionCon, self.trackCon)

    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        #print(results.pose_landmarks)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)

        return img

    def getPosition(self, img, draw=True):
        lmList= []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                #print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 7, (255, 0, 0), cv2.FILLED)
        return lmList

def main():
    # cap = cv2.VideoCapture('a.mp4')
    cap = cv2.VideoCapture(0)
    pTime = 0
    output = 0
    detector = PoseDetector()
    while True:
        success, img = cap.read()
        img = detector.findPose(img)
        lmList = detector.getPosition(img)
        if lmList:
            if lmList[1][1] < 200: # leaning right
                output = 1
                #print("1")
            elif lmList[1][1] > 450: # leaning left
                output = -1
                #print("-1")
            else: # not leaning
                output = 0
                #print("0")
        else: # out of frame
            output = 0
        

        cTime = time.time()
        #fps = 1 / (cTime - pTime)
        fps = 10
        pTime = cTime

        sock.SendData(str(output))
        # if(args['debug']):
        #     print(output)
        cv2.putText(img, str(int(fps)), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()