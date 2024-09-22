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
poses_names=["pranamasana","hastauttanasana","hastapadasana","right_ashwa_sanchalanasana","dandasana","ashtanga_namaskara","bhujangasana","adho_mukha_svanasana","ashwa_sanchalanasana"]
asana_to_joint=detector.map_asana_joints()
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
    def compare_poses(self, landmarks1, landmarks2):
        total_distance = 0
        for i in range(len(landmarks1)):
            total_distance += self.euclidean_distance(landmarks1[i], landmarks2[i])
        avg_distance = total_distance / len(landmarks1)
        return avg_distance
    
    def get_wrong_joints(self, asana,correct_landmarks, input_landmarks, thresh):
        
        

        correct_landmark_dict = detector.map_landmarks(correct_landmarks)
        correct_joints_dict = detector.map_joints(correct_landmark_dict)
        correct_joints_dict=detector.get_joints_for_asana(asana,asana_to_joint,correct_joints_dict)

        input_landmark_dict = detector.map_landmarks(input_landmarks)
        input_joints_dict = detector.map_joints(input_landmark_dict)
        input_joints_dict=detector.get_joints_for_asana(asana,asana_to_joint,input_joints_dict)

        wrong_joints = {}
        for i in correct_joints_dict:
            correct_angle = detector.calculate_angle(correct_joints_dict[i])
            input_angle = detector.calculate_angle(input_joints_dict[i])
            diff = correct_angle - input_angle
            if(abs(diff)>thresh):
                if(diff>0):
                    wrong_joints[i] =  (diff, correct_angle, input_angle, "increase")
                else:
                    wrong_joints[i] = (diff, correct_angle, input_angle, "decrease")
        return wrong_joints

def resize_image(image, max_width=800, max_height=600):
    height, width = image.shape[:2]
    if width > max_width or height > max_height:
        scaling_factor = min(max_width / width, max_height / height)
        new_size = (int(width * scaling_factor), int(height * scaling_factor))
        return cv.resize(image, new_size)
    return image




if __name__ == "__main__":
    # Example usage
    pose_sim = PoseSimilarity()
    
    
    #asana=input()
    # orientations=["_straight","_left","_right"]
    # asanas_dict={}
    # lmlists=[]
    # Example usage with your images
    # for i in orientations:
    # for asana in poses_names:
    asana="parvatasana"
    print("ideal_landmarks["+'"'+asana+'"'+"] = []")
    for i in range(3):
        frame1 = cv.imread(asana+"("+str(i+1)+")"+".jpg")
        # if(i == 0):
        #     frame1 = cv.imread(asana+"("+str(i+1)+")"+".jpg")
        # else:
        #     frame1 = cv.imread(asana+"("+str(i+1)+")"+".jpeg")
        frame1 = resize_image(frame1)
    #cv.imshow("Without_detection", frame1_resized)
        frame1 = detector.findPose(frame1)
        lmlist1 = detector.findPosition(frame1)
        normalized_landmarks1 = pose_sim.normalize_landmarks(lmlist1, reference_idx=0)
        print("absolutely_ideal_landmarks["+'"'+asana+'"'+"].append("+str(normalized_landmarks1)+")")
        print("\n")
    #     lmlists.append(lmlist1)
    # asanas_dict[asana]=lmlists
    frame2 = cv.imread("wrong_padmasana.jpeg")
    frame2 = resize_image(frame2)
    frame2 = detector.findPose(frame2)
    lmlist2 = detector.findPosition(frame2)
    cv.imshow("Corrected_padmasana", frame1)
    cv.imshow("Wrong_padmasana", frame2)
    #Example landmarks for two poses (these should be passed in from another part of your code)
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
    
    # print("landmarks1: ", landmarks1)
    # print("lmlist1: ", lmlist1)
    # print("landmarks2: ", landmarks2)
    # print("lmlist2: ", lmlist2)




    # Normalize landmarks with respect to a reference point (e.g., left hip index = 24)
    normalized_landmarks1 = pose_sim.normalize_landmarks(lmlist1, reference_idx=0)
    normalized_landmarks2 = pose_sim.normalize_landmarks(lmlist2, reference_idx=0)
    
    # Compare the poses
    wrong_joints = pose_sim.get_wrong_joints(normalized_landmarks1, normalized_landmarks2, 20)
    for i in wrong_joints:
        print(i, wrong_joints[i])
    ctime = time.time()
    print(ctime-ptime)
    #print("Poses are similar" if are_similar else "Poses are different")
    cv.waitKey(100000)
