import cv2 as cv
import mediapipe as mp
import time
import numpy as np


class PoseDetector:
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
    
    def map_landmarks(self, landmarks):
        landmark_dict = {
        'nose': landmarks[0],
        'left_eye_inner': landmarks[1],
        'left_eye': landmarks[2],
        'left_eye_outer': landmarks[3],
        'right_eye_inner': landmarks[4],
        'right_eye': landmarks[5],
        'right_eye_outer': landmarks[6],
        'left_ear': landmarks[7],
        'right_ear': landmarks[8],
        'mouth_left': landmarks[9],
        'mouth_right': landmarks[10],
        'left_shoulder': landmarks[11],
        'right_shoulder': landmarks[12],
        'left_elbow': landmarks[13],
        'right_elbow': landmarks[14],
        'left_wrist': landmarks[15],
        'right_wrist': landmarks[16],
        'left_pinky': landmarks[17],
        'right_pinky': landmarks[18],
        'left_index': landmarks[19],
        'right_index': landmarks[20],
        'left_thumb': landmarks[21],
        'right_thumb': landmarks[22],
        'left_hip': landmarks[23],
        'right_hip': landmarks[24],
        'left_knee': landmarks[25],
        'right_knee': landmarks[26],
        'left_ankle': landmarks[27],
        'right_ankle': landmarks[28],
        'left_heel': landmarks[29],
        'right_heel': landmarks[30],
        'left_foot_index': landmarks[31],
        'right_foot_index': landmarks[32],
        'mid_hip': ((landmarks[23][0]+landmarks[24][0])/2, (landmarks[23][1]+landmarks[24][1])/2),
        'neck': ((landmarks[11][0]+landmarks[12][0])/2, (landmarks[11][1]+landmarks[12][1])/2)
        
    }
        return landmark_dict
    
    def map_joints(self, landmark_dict):
        joint_dict = {
        "left_knee_joint": [landmark_dict['left_ankle'], landmark_dict['left_knee'], landmark_dict['left_hip']],
        "right_knee_joint": [landmark_dict['right_ankle'], landmark_dict['right_knee'], landmark_dict['right_hip']],
        "left_hip_joint": [landmark_dict['left_knee'], landmark_dict['left_hip'], landmark_dict['left_shoulder']],
        "right_hip_joint": [landmark_dict['right_knee'], landmark_dict['right_hip'], landmark_dict['right_shoulder']],
        "left_shoulder_joint": [landmark_dict['left_elbow'], landmark_dict['left_shoulder'], landmark_dict['left_hip']],
        "right_shoulder_joint": [landmark_dict['right_elbow'], landmark_dict['right_shoulder'], landmark_dict['right_hip']],
        "neck": [landmark_dict['mid_hip'], landmark_dict['neck'], landmark_dict['nose']],
        "leg_angle": [landmark_dict['left_knee'], landmark_dict['mid_hip'], landmark_dict['right_knee']],
        "left_ankle_joint": [landmark_dict['left_knee'], landmark_dict['left_ankle'], landmark_dict['left_foot_index']],
        "right_ankle_joint": [landmark_dict['right_knee'], landmark_dict['right_ankle'], landmark_dict['right_foot_index']],
        "left_elbow": (landmark_dict['left_shoulder'], landmark_dict['left_elbow'], landmark_dict['left_wrist']),
        "right_elbow": (landmark_dict['right_shoulder'], landmark_dict['right_elbow'], landmark_dict['right_wrist'])
    }
        return joint_dict


    
    def calculate_angle(self, points):
        """
        Calculate the angle between three points a, b, and c.
        a: The first point (shoulder).
        b: The vertex point (elbow).
        c: The second point (wrist).
        """
        if(points != None):
            a = np.array(points[0])  # Shoulder
            b = np.array(points[1])  # Elbow
            c = np.array(points[2])  # Wrist

        # Calculate the vectors
            ba = a - b  # Vector from shoulder to elbow
            bc = c - b  # Vector from elbow to wrist

                # Calculate the angle using the dot product
            cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
            angle = np.arccos(cosine_angle)  # Angle in radians

            return np.degrees(angle)  # Convert to degrees
        else:
            print("No points given")
    
    

    



        
            


    


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