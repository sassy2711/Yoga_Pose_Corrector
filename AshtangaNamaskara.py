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


ashtanganamaskara1 = cv.imread("AshtangaNamaskaraFlipped.png")
ashtanganamaskara1 = detector.findPose(ashtanganamaskara1)
landmarks1 = detector.findPosition(ashtanganamaskara1)
resized_ashtanganamaskara = cv.resize(ashtanganamaskara1, (800,600))
print("landmarks1: ", landmarks1)
cv.imshow("Test", resized_ashtanganamaskara)

ashtanganamaskara2 = cv.imread("AshtangaNamaskara2.jpg")
ashtanganamaskara2 = detector.findPose(ashtanganamaskara2)
landmarks2 = detector.findPosition(ashtanganamaskara2)
print("landmarks2: ", landmarks2)

ashtanganamaskara3 = cv.imread("AshtangaNamaskara3.jpeg")
ashtanganamaskara3 = detector.findPose(ashtanganamaskara3)
landmarks3 = detector.findPosition(ashtanganamaskara3)
print("landmarks3: ", landmarks3)

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

        if len(lmlist)>0:
            knee_angle = angle(lmlist[24], lmlist[26], lmlist[28])
            # print(knee_angle)
            # print(f'lefthip: {lmlist[24]}, leftknee: {lmlist[26]}')
            # print(f'leftshoulder: {lmlist[12]}, leftknee: {lmlist[26]}')
            if PoseSimilarityDetector.compare_poses(landmarks1, lmlist, threshold=0.2) or PoseSimilarityDetector.compare_poses(landmarks2, lmlist, threshold=0.2) or PoseSimilarityDetector.compare_poses(landmarks3, lmlist, threshold=0.2):
                if (abs(lmlist[26][1]-lmlist[12][1])>0.06):
                    print("Please lie on the ground.")
                elif(abs(lmlist[24][1]-lmlist[26][1])<0.04):
                    print("Please rise your hip.")
                else:
                    print("You are doing the right asana.")
            else:
                print("Your are doing the wrong asana, Please see the images provided.")

    ctime =  time.time()
    # print("time: ", ctime-ptime)
    ptime = ctime
    cv.imshow("AshtangaNamaskaraCheck", frame)
    cv.waitKey(10)

cv.destroyAllWindows()
