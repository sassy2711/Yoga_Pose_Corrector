import cv2 as cv
import PoseModule as pm
import mediapipe as mp
import numpy as np
import pose_equal_check as pec
import time

ctime = 0
ptime = time.time()

vid = cv.VideoCapture(0)
detector = pm.PoseDetector()
PoseSimilarityDetector = pec.PoseSimilarity()

dandanasana1 = cv.imread("Dandanasana5.png")
dandanasana1 = detector.findPose(dandanasana1)
landmarks1 = detector.findPosition(dandanasana1)
print("landmarks1: ", landmarks1)
cv.imshow("Dandasana1", dandanasana1)

dandanasana2 = cv.imread("Dandanasana7.png")
dandanasana2 = detector.findPose(dandanasana2)
landmarks2 = detector.findPosition(dandanasana2)
print("landmarks2: ", landmarks2)
cv.imshow("Dandasana2", dandanasana2)

dandanasana3 = cv.imread("Dandanasana6.png")
dandanasana3 = detector.findPose(dandanasana3)
landmarks3 = detector.findPosition(dandanasana3)
print("landmarks3: ", landmarks3)
cv.imshow("Dandasana3", dandanasana3)

Chaitudandanasana1 = cv.imread("ChaituDandanasana1.jpg")
Chaitudandanasana1 = detector.findPose(Chaitudandanasana1)
Chaitulandmarks1 = detector.findPosition(Chaitudandanasana1)
cv.imshow("Chaitudandanasana1", Chaitudandanasana1)

Tahirpranamasana2 = cv.imread("TahirPranamasana2.jpg")
Tahirpranamasana2 = detector.findPose(Tahirpranamasana2)
Tahirlandmarks2 = detector.findPosition(Tahirpranamasana2)

def angle(a,b,c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

     # Calculate the vectors
    ab = a-b  # Vector from shoulder to elbow
    bc = b-c  # Vector from elbow to wrist

    # Calculate the angle using the dot product
    cosine_angle = np.dot(ab, bc) / (np.linalg.norm(ab) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)  # Angle in radians

    return 180 - np.degrees(angle)  # Convert to degrees



while True:
    isTrue, frame = vid.read() 

    if isTrue:
        frame = detector.findPose(frame)
        lmlist = detector.findPosition(frame)
        
# or PoseSimilarityDetector.compare_poses(Tahirlandmarks1, lmlist, threshold=0.1) or PoseSimilarityDetector.compare_poses(Tahirlandmarks2, lmlist, threshold=0.1)
        if len(lmlist)>0:
            left_knee_angle = angle(lmlist[24], lmlist[26], lmlist[28])
            right_knee_angle = angle(lmlist[23], lmlist[25], lmlist[27])
            # print(f'left_knee_angle: {left_knee_angle}, right_knee)angle: {right_knee_angle}')
            if PoseSimilarityDetector.compare_poses(landmarks1, lmlist, threshold=0.2) or PoseSimilarityDetector.compare_poses(landmarks2, lmlist, threshold=0.2) or PoseSimilarityDetector.compare_poses(landmarks3, lmlist, threshold=0.2):
                if(left_knee_angle<160 or right_knee_angle<150):
                    print("Please keep your legs straight.")
                else:
                    print("You are doing the right Pose.")    
            else:
                print("Your are doing the wrong asana, Please see the image")

    ctime =  time.time()
    # print("time: ", ctime-ptime
    ptime = ctime
    cv.imshow("DandanasanaCheck", frame)
    cv.waitKey(10)

cv.destroyAllWindows()
