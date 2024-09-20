import numpy as np
import cv2 as cv
import mediapipe as mp
import numpy as np
import time
import PoseModule as pm
# Initialize MediaPipe Pose Detection
detector = pm.PoseDetector()
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils
ctime =0
ptime = time.time()
class PoseSimilarity():
    # Function to calculate Euclidean distance between two points
    def euclidean_distance(self, point1, point2):
        return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    
    # Function to normalize key points based on a reference point
    def normalize_landmarks(self, landmarks, reference_idx):
        ref_point = landmarks[reference_idx]
        normalized_landmarks = [(point[0] - ref_point[0], point[1] - ref_point[1]) for point in landmarks]
        return normalized_landmarks
    
    # Function to compare two sets of pose landmarks
    def compare_poses(self, landmarks1, landmarks2, threshold=0.1):
        total_distance = 0
        for i in range(len(landmarks1)):
            total_distance += self.euclidean_distance(landmarks1[i], landmarks2[i])
        avg_distance = total_distance / len(landmarks1)
        return avg_distance < threshold

if __name__ == "__main__":
    # Example usage
    pose_sim = PoseSimilarity()
    
    

    frame1 = cv.imread("Padmasana.jpeg")
    frame1 = detector.findPose(frame1)
    lmlist1 = detector.findPosition(frame1)
    frame2 = cv.imread("Tarun_padmasana.jpg")
    frame2 = detector.findPose(frame2)
    lmlist2 = detector.findPosition(frame2)
    # Example landmarks for two poses (these should be passed in from another part of your code)
    frame_rgb1 = cv.cvtColor(frame1, cv.COLOR_BGR2RGB)
    result1 = pose.process(frame_rgb1)
    landmarks1 = []
    if result1.pose_landmarks:
        for lm in result1.pose_landmarks.landmark:
            landmarks1.append((lm.x, lm.y))

    frame_rgb2 = cv.cvtColor(frame2, cv.COLOR_BGR2RGB)
    result2 = pose.process(frame_rgb2)
    landmarks2 = []
    if result2.pose_landmarks:
        for lm in result2.pose_landmarks.landmark:
            landmarks2.append((lm.x, lm.y))
    
    print("landmarks1: ", landmarks1)
    print("lmlist1: ", lmlist1)
    print("landmarks2: ", landmarks2)
    print("lmlist2: ", lmlist2)




    # Normalize landmarks with respect to a reference point (e.g., left hip index = 24)
    normalized_landmarks1 = pose_sim.normalize_landmarks(lmlist1, reference_idx=0)
    normalized_landmarks2 = pose_sim.normalize_landmarks(lmlist2, reference_idx=0)
    
    # Compare the poses
    are_similar = pose_sim.compare_poses(normalized_landmarks1, normalized_landmarks2, threshold=0.1)
    ctime = time.time()
    print(ctime-ptime)
    print("Poses are similar" if are_similar else "Poses are different")