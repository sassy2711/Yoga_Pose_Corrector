import cv2 as cv
import mediapipe as mp
import time
import numpy as np


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
    
    def map_landmarks(landmarks):
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
        'left_hip': landmarks[17],
        'right_hip': landmarks[18],
        'left_knee': landmarks[19],
        'right_knee': landmarks[20],
        'left_ankle': landmarks[21],
        'right_ankle': landmarks[22],
        'left_foot_index': landmarks[23],
        'right_foot_index': landmarks[24],
        'left_foot_outer': landmarks[25],
        'right_foot_outer': landmarks[26],
        'left_big_toe': landmarks[27],
        'right_big_toe': landmarks[28],
        'left_heel': landmarks[29],
        'right_heel': landmarks[30],
        'left_foot_arch': landmarks[31],
        'right_foot_arch': landmarks[32],
        'mid_hip': ((landmarks[17][0]+landmarks[18][0])/2, (landmarks[17][1]+landmarks[18][1])/2),
        'neck': ((landmarks[11][0]+landmarks[12][0])/2, (landmarks[11][1]+landmarks[12][1])/2)
    }
        return landmark_dict
    
    def map_joints():
        joint_dict = {
    "left_knee_joint": ["left_ankle", "left_knee", "left_hip"],
    "right_knee_joint": ["right_ankle", "right_knee", "right_hip"],
    "left_hip_joint": ["left_knee", "left_hip", "left_shoulder"],
    "right_hip_joint": ["right_knee", "right_hip", "right_shoulder"],
    "left_shoulder_joint": ["left_elbow", "left_shoulder", "left_hip"],
    "right_shoulder_joint": ["right_elbow", "right_shoulder", "right_hip"],
    "neck": ["mid_hip", "neck", "nose"],
    "leg_angle": ["left_knee", "mid_hip", "right_knee"]
    }
        return joint_dict

class Angles:
    landmarks_dict = {}
    joints_dict = {}
    
    def __init__(self,  landmark_dict, joints_dict):
        self.landmark_dict = landmark_dict
        self.joints_dict = joints_dict
    
    def calculate_angle(points):
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
            ab = b - a  # Vector from shoulder to elbow
            bc = c - b  # Vector from elbow to wrist

                # Calculate the angle using the dot product
            cosine_angle = np.dot(ab, bc) / (np.linalg.norm(ab) * np.linalg.norm(bc))
            angle = np.arccos(cosine_angle)  # Angle in radians

            return np.degrees(angle)  # Convert to degrees
        else:
            print("No points given")

    def get_joint_points(self, joint):
        """
        Given the joint name, return the indices of the three landmarks
        required to calculate the angle at that joint.
        """
        if joint in self.joints_dict:
            points = self.joints_dict[joint]
            return [self.landmarks_dict[point] for point in points]
        else:
            print("Joint not in dict.")
            return None



            


    


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