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
import mediapipe as mp
import pose_equal_check as pec
warnings.filterwarnings("ignore", category=UserWarning, module="google.protobuf.symbol_database")

#In lmlist 0th cordinate is x coordinate and 1st coordinate is y coordinate.


ptime = 0
ctime = 0 
detector = pm.PoseDetector()
mpPose = mp.solutions.pose
pose = mpPose.Pose()   # I was getting some errors while passing the parameters here so i didn't pass them here
mpDraw = mp.solutions.drawing_utils
poseEqualityDetector = pec.PoseSimilarity()
# st.set_page_config(page_title="Streamlit check")
# st.header("Streamlit")


# Placeholde for image
# img_placeholder = st.empty() 


def isStraightline(a, b, c):
    try:
        m1 = (b[1] - a[1]) / (b[0] - a[0])
    except ZeroDivisionError:
        m1 = float('inf')  # Use infinity to represent an undefined slope

    try:
        m2 = (b[1] - c[1]) / (c[0] - a[0])
    except ZeroDivisionError:
        m2 = float('inf')  # Use infinity to represent an undefined slope

    if m1 == float('inf') or m2 == float('inf'):
        if m1 == m2:
            return 0  # Collinear if both slopes are infinity and equal
        else:
            return float('inf')  # Not collinear if slopes are different
        
    print(m1, m2)

    angle = math.atan(abs((m1 - m2) / (1 + m1 * m2)))

    return angle

def isright(lmlist):
    if (lmlist[31][0] < lmlist[30][0] and abs(lmlist[12][0]-lmlist[11][0])<75):
        return True
    print("Please turn to your right side.")
    return False

def isMountainPose(landmarks):
    asana = cv.imread("Padmasana.jpeg")
    asana = cv.flip(asana, 1)
    asana = detector.findPose(asana)
    landmarks1 = detector.findPosition(asana)
    if len(landmarks1)>0:
        return poseEqualityDetector.compare_poses(landmarks1, landmarks)
    return -1


pygame.mixer.init()

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



text_to_speech("Program Starting.")

last_Speech_time = time.time()
vid = cv.VideoCapture(0)
while True:
    isTrue, frame = vid.read()
    
    if isTrue:

        current_time = time.time()
        if((current_time-last_Speech_time)>5):
            print("Creating Thread")
            threading.Thread(target=text_to_speech, args=("Keep going!",)).start()
            last_Speech_time = current_time

        original_height, original_width = frame.shape[:2]

        # Define a scale factor (e.g., 0.5 for half the size)
        scale_factor = 1.5

        # Calculate the new dimensions while maintaining the aspect ratio
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)
        
        # Resize the frame while maintaining the aspect ratio
        frame = cv.resize(frame, (new_width, new_height), interpolation=cv.INTER_AREA)


        frame = detector.findPose(frame)
        lmlist = detector.findPosition(frame)

        

        ctime = time.time()
        fps = 1/(ctime-ptime)
        ptime = ctime
        cv.putText(frame, str(f'{int(fps)} FPS'), (30, 40), cv.FONT_HERSHEY_PLAIN, 1.7, (0,255,0), thickness=3)
        # webImg = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        # img_placeholder.image(webImg, caption="MYImage")

        if len(lmlist)>0:
            if(isMountainPose(lmlist)):
                frame = detector.ChangeColor(frame)
         
        cv.imshow('Video', frame)

        if cv.waitKey(10) and 0xFF == ord('q'):
            break
        # cv.waitKey(10)
cv.destroyAllWindows()