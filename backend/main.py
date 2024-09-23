import cv2 as cv
import time
import PoseModule as pm
# import streamlit as st
import threading
import math
import pygame
import gtts as gTTS
import io
import warnings
import numpy as np
import mediapipe as mp
import pose_equal_check as pec
warnings.filterwarnings("ignore", category=UserWarning, module="google.protobuf.symbol_database")

#In input_landmarks 0th cordinate is x coordinate and 1st coordinate is y coordinate.
detector = pm.PoseDetector()
mpPose = mp.solutions.pose
pose = mpPose.Pose()   # I was getting some errors while passing the parameters here so i didn't pass them here
mpDraw = mp.solutions.drawing_utils
poseEqualityDetector = pec.PoseSimilarity()
pygame.mixer.init()


PoseSimilarity = pec.PoseSimilarity()

def text_to_speech(text):
    """Plays TTS audio without reinitializing pygame mixer."""
    try:
        # Convert the text to speech using gTTS (Google TTS)
        tts = gTTS.gTTS(text=text, lang='en-in')

        # Create an in-memory file for the speech
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)

        # Play the speech using pygame
        pygame.mixer.music.load(mp3_fp, 'mp3')
        pygame.mixer.music.play()

        # Do not block the thread, check periodically
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

    except Exception as e:
        print(f"Error in text_to_speech: {e}")


def menu():
    print("Choose an asana:")
    print("1. pranamasana\n2. hastauttanasana\n3. hastapadasana\n4. right_ashwa_sanchalanasana\n5. left_ashwa_sanchalanasana\n6. dandasana\n7. ashtanga_namaskara\n8. bhujangasana \n9. adho_mukha_svanasana")

text_to_speech("Program Starting.")

menu()
pose_name = input()
last_check_time = time.time()
vid = cv.VideoCapture(0)

while True:
    isTrue, input_frame = vid.read()
    
    if isTrue:
        original_height, original_width = input_frame.shape[:2]

        # Define a scale factor (e.g., 0.5 for half the size)
        scale_factor = 1.5

        # Calculate the new dimensions while maintaining the aspect ratio
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)
        
        # Resize the input_frame while maintaining the aspect ratio
        input_frame = cv.resize(input_frame, (new_width, new_height), interpolation=cv.INTER_AREA)


        input_frame = detector.findPose(input_frame)
        input_landmarks = detector.findPosition(input_frame)
        if(len(input_landmarks) == 0):
            continue
        input_landmarks = PoseSimilarity.normalize_landmarks(input_landmarks, reference_idx=0)
        # pose_name = "hastapadasana"
        current_time = time.time()
        if((current_time-last_check_time)>5 and len(input_landmarks)>0):
            last_check_time = current_time
            (isSimilar, correct_landmarks) = PoseSimilarity.isSimilar(pose_name, input_landmarks, 0.1)
            if(isSimilar):
                wrong_joints = PoseSimilarity.get_wrong_joints(pose_name, correct_landmarks, input_landmarks, 15)
                if(len(wrong_joints) == 0):
                    text = "You're doing it absolutely right."
                    threading.Thread(target=text_to_speech, args=(text,)).start()
                else:
                    text = []
                    for i in wrong_joints:
                        joint = wrong_joints[i][0]
                        change = wrong_joints[i][1]
                        text.append(change + "angle at" + " ".join((joint.split("_"))))
                    for i in text:
                        threading.Thread(target=text_to_speech, args=(i,)).start()
            else:
                text = "Thoda galat."
                threading.Thread(target=text_to_speech, args=(text,)).start()
        

        cv.imshow('Video', input_frame)

        if cv.waitKey(10) and 0xFF == ord('q'):
            break
        
cv.destroyAllWindows()
