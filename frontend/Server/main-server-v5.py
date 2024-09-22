import cv2 as cv
import time
import PoseModule as pm
# import streamlit as st
import threading
import math
import pygame
import gtts as gTTS

import io
import base64
import asyncio
import websockets
import json

import warnings
import numpy as np
import mediapipe as mp
import pose_equal_check as pec
warnings.filterwarnings("ignore", category=UserWarning, module="google.protobuf.symbol_database")

#In input_landmarks 0th cordinate is x coordinate and 1st coordinate is y coordinate.
detector = pm.PoseDetector()
mpPose = mp.solutions.pose
poseEqualityDetector = pec.PoseSimilarity()
pygame.mixer.init()

PoseSimilarity = pec.PoseSimilarity()
global last_check_time 

num_to_asana = {
    1 : "pranamasana",
    2 : "hastauttanasana",
    3 : "hastapadasana",
    4 : "right_ashwa_sanchalanasana",
    5 : "left_ashwa_sanchalanasana",
    6 : "dandasana",
    7 : "ashtanga_namaskara",
    8 : "bhujangasana",
    9 : "adho_mukha_svanasana",
}

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

def asanaCheck(asanaNum, input_landmarks):
    if len(input_landmarks) > 0:
        (isSimilar, _ ) = PoseSimilarity.isSimilar(num_to_asana[asanaNum], input_landmarks, 0.1)
        if (isSimilar):
            print('correct pose')
            return 2
        else:
            print('wrong pose')
            return 1
    return 0

def FeedbackTTS(asanaCheckOutput, asanaNum, input_landmarks):
    current_time = time.time()
    if (current_time - last_check_time) > 5:
        last_check_time = current_time
        if asanaCheckOutput == 1:
            text = "Thoda galat."
            threading.Thread(target=text_to_speech, args=(text,)).start()
            return
        
        elif asanaCheckOutput == 2:
            ( _ , correct_landmarks) = PoseSimilarity.isSimilar(num_to_asana[asanaNum], input_landmarks, 0.1)
            wrong_joints = PoseSimilarity.get_wrong_joints(num_to_asana[asanaNum], correct_landmarks, input_landmarks, 15)
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

        




def bytes_to_cv_image(byte_stream):
    # Convert BytesIO object to a NumPy array
    byte_array = np.frombuffer(byte_stream.getvalue(), np.uint8)

    # Decode the image using OpenCV
    image = cv.imdecode(byte_array, cv.IMREAD_COLOR)

    return image

async def websocket_handler(websocket, path):
    try:
        async for message in websocket:
            response = recognize_asana(message)
            await websocket.send(json.dumps(response))
    except Exception as e:
        print(f"WebSocket Error: {str(e)}")

def recognize_asana(message):
    try:
        # Decode the incoming message from JSON
        decoded_message = json.loads(message)

        # Extract the asana number and image data
        asana_number = decoded_message.get('asanaNumber')
        image_data = decoded_message.get('imageData')

        if image_data is None:
            return {"status": False, "message": "No image data provided", "data": 0}

        # Decode the base64 image data
        image_bytes = base64.b64decode(image_data)
        frame = io.BytesIO(image_bytes)

        # Convert the byte stream to a CV image
        cv_image = bytes_to_cv_image(frame)

        if cv_image is None:
            return {"status": False, "message": "Failed to decode image", "data": 0}

        # Process the image with your pose detection logic
        frame2 = detector.findPose(cv_image)
        input_landmarks = detector.findPosition(frame2)
        input_landmarks = PoseSimilarity.normalize_landmarks(input_landmarks, reference_idx=0)

        # You can now use asana_number and lmlist for further processing
        # Add your logic here to evaluate the pose and return the result


        #New Code:
        # if(len(input_landmarks) == 0):
        #     return {"status": True, "message": "No Asana Detected", "data": 0}
        
        # input_landmarks = PoseSimilarity.normalize_landmarks(input_landmarks, reference_idx = 0)

        # current_time = time.time()
        # pose_name = num_to_asana[asana_number]
        # if((current_time - last_check_time)>5 and len(input_landmarks)>0):
        #     last_check_time = current_time
        #     (isSimilar, correct_landmarks) = PoseSimilarity.isSimilar(pose_name, input_landmarks, 0.1)
        #     if(isSimilar):
        #         wrong_joints = PoseSimilarity.get_wrong_joints(pose_name, correct_landmarks, input_landmarks, 15)
        #         if(len(wrong_joints) == 0):
        #             text = "You're doing it absolutely right."
        #             threading.Thread(target=text_to_speech, args=(text,)).start()
        #             return {"status": True, "message": "Recognition successful", "data": 2}
        #         else:
        #             text = []
        #             for i in wrong_joints:
        #                 joint = wrong_joints[i][0]
        #                 change = wrong_joints[i][1]
        #                 text.append(change + "angle at" + " ".join((joint.split("_"))))
        #             for i in text:
        #                 threading.Thread(target=text_to_speech, args=(i,)).start()
        #             return {"status": True, "message": "Recognition unsuccessful", "data": 1}
        #     else:
        #         text = "Thoda galat."
        #         threading.Thread(target=text_to_speech, args=(text,)).start()
        #         return {"status": True, "message": "No Asana Detected", "data": 0}
            

        #Old Code:
        status = asanaCheck(asana_number, input_landmarks)

        # FeedbackTTS(status, asana_number, input_landmarks)
        # current_time = time.time()
        # pose_name = num_to_asana[asana_number]
        # if((current_time-last_check_time)>5 and len(input_landmarks)>0):
        #     #global last_check_time 
        #     last_check_time = current_time
        #     (isSimilar, correct_landmarks) = PoseSimilarity.isSimilar(pose_name, input_landmarks, 0.1)
        #     if(isSimilar):
        #         wrong_joints = PoseSimilarity.get_wrong_joints(pose_name, correct_landmarks, input_landmarks, 15)
        #         if(len(wrong_joints) == 0):
        #             text = "You're doing it absolutely right."
        #             threading.Thread(target=text_to_speech, args=(text,)).start()
        #         else:
        #             text = []
        #             for i in wrong_joints:
        #                 joint = wrong_joints[i][0]
        #                 change = wrong_joints[i][1]
        #                 text.append(change + "angle at" + " ".join((joint.split("_"))))
        #             for i in text:
        #                 threading.Thread(target=text_to_speech, args=(i,)).start()
        #     else:
        #         text = "Thoda galat."
        #         threading.Thread(target=text_to_speech, args=(text,)).start()

        if status == 0:
            return {"status": True, "message": "No Asana Detected", "data": 0}
        if status == 2:
            return {"status": True, "message": "Recognition successful", "data": 2}
        else:
            return {"status": True, "message": "Recognition unsuccessful", "data": 1}

        # return {"status": True, "message": "Pose recognized", "asanaNumber": asana_number, "data": lmlist}

    except json.JSONDecodeError:
        return {"status": False, "message": "Invalid JSON format", "data": 0}
    except Exception as e:
        return {"status": False, "message": str(e), "data": 0}



if __name__ == '__main__':
    text_to_speech("Program Starting.")
    last_check_time = time.time()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        websockets.serve(websocket_handler, "0.0.0.0", 8765)
    )
    loop.run_forever()




# input_frame = detector.findPose(input_frame)
# input_landmarks = detector.findPosition(input_frame)
# if(len(input_landmarks) == 0):
#     continue
# input_landmarks = PoseSimilarity.normalize_landmarks(input_landmarks, reference_idx=0)

# current_time = time.time()
# pose_name = "pranamasana"
# if((current_time-last_check_time)>5 and len(input_landmarks)>0):
#     last_check_time = current_time
#     (isSimilar, correct_landmarks) = PoseSimilarity.isSimilar(pose_name, input_landmarks, 0.1)
#     if(isSimilar):
#         wrong_joints = PoseSimilarity.get_wrong_joints(pose_name, correct_landmarks, input_landmarks, 15)
#         if(len(wrong_joints) == 0):
#             text = "You're doing it absolutely right."
#             threading.Thread(target=text_to_speech, args=(text,)).start()
#         else:
#             text = []
#             for i in wrong_joints:
#                 joint = wrong_joints[i][0]
#                 change = wrong_joints[i][1]
#                 text.append(change + "angle at" + " ".join((joint.split("_"))))
#             for i in text:
#                 threading.Thread(target=text_to_speech, args=(i,)).start()
#     else:
#         text = "Thoda galat."
#         threading.Thread(target=text_to_speech, args=(text,)).start()






# last_check_time = time.time()
# vid = cv.VideoCapture(0)
# while True:
#     isTrue, input_frame = vid.read()
    
#     if isTrue:
#         original_height, original_width = input_frame.shape[:2]

#         # Define a scale factor (e.g., 0.5 for half the size)
#         scale_factor = 1.5

#         # Calculate the new dimensions while maintaining the aspect ratio
#         new_width = int(original_width * scale_factor)
#         new_height = int(original_height * scale_factor)
        
#         # Resize the input_frame while maintaining the aspect ratio
#         input_frame = cv.resize(input_frame, (new_width, new_height), interpolation=cv.INTER_AREA)


#         input_frame = detector.findPose(input_frame)
#         input_landmarks = detector.findPosition(input_frame)
#         if(len(input_landmarks) == 0):
#             continue
#         input_landmarks = PoseSimilarity.normalize_landmarks(input_landmarks, reference_idx=0)

#         current_time = time.time()
#         pose_name = "pranamasana"
#         if((current_time-last_check_time)>5 and len(input_landmarks)>0):
#             last_check_time = current_time
#             (isSimilar, correct_landmarks) = PoseSimilarity.isSimilar(pose_name, input_landmarks, 0.1)
#             if(isSimilar):
#                 wrong_joints = PoseSimilarity.get_wrong_joints(pose_name, correct_landmarks, input_landmarks, 15)
#                 if(len(wrong_joints) == 0):
#                     text = "You're doing it absolutely right."
#                     threading.Thread(target=text_to_speech, args=(text,)).start()
#                 else:
#                     text = []
#                     for i in wrong_joints:
#                         joint = wrong_joints[i][0]
#                         change = wrong_joints[i][1]
#                         text.append(change + "angle at" + " ".join((joint.split("_"))))
#                     for i in text:
#                         threading.Thread(target=text_to_speech, args=(i,)).start()
#             else:
#                 text = "Thoda galat."
#                 threading.Thread(target=text_to_speech, args=(text,)).start()
                
                

        # ctime = time.time()
        # fps = 1/(ctime-ptime)
        # ptime = ctime
        # cv.putText(input_frame, str(f'{int(fps)} FPS'), (30, 40), cv.FONT_HERSHEY_PLAIN, 1.7, (0,255,0), thickness=3)
        # webImg = cv.cvtColor(input_frame, cv.COLOR_BGR2RGB)
        # img_placeholder.image(webImg, caption="MYImage")

        
         
        # cv.imshow('Video', input_frame)

        # if cv.waitKey(10) and 0xFF == ord('q'):
        #     break
        # # cv.waitKey(10)
        # cv.destroyAllWindows()