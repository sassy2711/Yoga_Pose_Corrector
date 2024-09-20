import cv2 as cv
import mediapipe as mp
import time


class PoseDetector():
    def __init__(self, mode=False, upBody=False, smooth=True,
                  detectionCon = 0.5, trackCon=0.5):
        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose()   # I was getting some errors while passing the parameters here so i didn't pass them here

        self.mpDraw = mp.solutions.drawing_utils


    def findPose(self, frame, draw = True):
        self.imgRGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        self.results = self.pose.process(self.imgRGB)
        if self.results.pose_landmarks:
            if draw:
                landmark_style = self.mpDraw.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=2)
                connection_style = self.mpDraw.DrawingSpec(color=(255,255,255), thickness=2)
                self.mpDraw.draw_landmarks(frame, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS,landmark_drawing_spec=landmark_style, connection_drawing_spec=connection_style)
        
        return frame
    
    def findPosition(self, frame, draw = False):
        lmlist = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([lm.x, lm.y])
                if draw:
                    cv.putText(frame, str(id), (cx, cy), cv.FONT_HERSHEY_PLAIN, 1.0, (255,255,255), thickness=2)
        return lmlist
    
    def ChangeColor(self, frame, color=(0,255,0), draw=True):
        if self.results.pose_landmarks:
            if draw:
                landmark_style = self.mpDraw.DrawingSpec(color=(0,0,255), thickness=2, circle_radius=2)
                connection_style = self.mpDraw.DrawingSpec(color=color, thickness=2)
                self.mpDraw.draw_landmarks(frame, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS,landmark_drawing_spec=landmark_style, connection_drawing_spec=connection_style)
        
        return frame

    
       

            


    


def main():
    vid = cv.VideoCapture(-1)
    ptime = 0
    ctime = 0 
    detector = PoseDetector()

    while True:
        isTrue, frame = vid.read()
        frame = detector.findPose(frame)
        lmlist = detector.findPosition(frame)


        ctime = time.time()
        fps = 1/(ctime-ptime)
        ptime = ctime
        cv.putText(frame, str(f'{int(fps)} FPS'), (30, 40), cv.FONT_HERSHEY_PLAIN, 1.7, (0,255,0), thickness=3)
        cv.imshow('Video', frame)

        cv.waitKey(10)

if __name__ == "__main__":
    main()