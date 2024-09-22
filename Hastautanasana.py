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

hastautanasana1 = cv.imread("Hastautanasana1.jpg")
hastautanasana1 = detector.findPose(hastautanasana1)
landmarks1 = detector.findPosition(hastautanasana1)
print("landmarks1: ", landmarks1)
cv.imshow("Hastautanasana1", hastautanasana1)

hastautanasana2 = cv.imread("Hastautanasana2.jpg")
hastautanasana2 = detector.findPose(hastautanasana2)
landmarks2 = detector.findPosition(hastautanasana2)
print("landmarks2: ", landmarks2)
cv.imshow("Hastautanasana2", hastautanasana2)

hastautanasana3 = cv.imread("Hastautanasana3.jpg")
hastautanasana3 = detector.findPose(hastautanasana3)
landmarks3 = detector.findPosition(hastautanasana3)
print("landmarks3: ", landmarks3)
cv.imshow("Hastautanasana3", hastautanasana3)

Tahirpranamasana1 = cv.imread("TahirPranamasana1.jpg")
Tahirpranamasana1 = detector.findPose(Tahirpranamasana1)
Tahirlandmarks1 = detector.findPosition(Tahirpranamasana1)

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
            if PoseSimilarityDetector.compare_poses(landmarks1, lmlist, threshold=0.1) or PoseSimilarityDetector.compare_poses(landmarks2, lmlist, threshold=0.1) or PoseSimilarityDetector.compare_poses(landmarks3, lmlist, threshold=0.1):
                print("You are doing the right Pose.")    
            else:
                print("Your are doing the wrong asana, Please see the images provided.")

    ctime =  time.time()
    # print("time: ", ctime-ptime)
    ptime = ctime
    cv.imshow("HastautanasanaCheck", frame)
    cv.waitKey(10)

cv.destroyAllWindows()
