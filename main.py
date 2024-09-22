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
# uttanasana = cv.imread("idealAsanas\ArdhaUttanasana.jpeg")
# uttanasana = detector.findPose(uttanasana)
# landmarks = detector.findPosition(uttanasana)

Uttanasanalandmarks = [[0.41045868396759033, 0.48211175203323364], [0.39815905690193176, 0.4574122726917267], [0.398689866065979, 0.45233598351478577], [0.3991246223449707, 0.44679465889930725], [0.39799967408180237, 0.45943737030029297], [0.39840996265411377, 0.45586422085762024], [0.398605614900589, 0.4516432285308838], [0.4119645953178406, 0.40806397795677185], [0.40817418694496155, 0.4135401248931885], [0.4254474639892578, 0.4723151624202728], [0.4262276887893677, 0.47531741857528687], [0.4760311543941498, 0.39740100502967834], [0.4873851537704468, 0.3800548315048218], [0.5216138958930969, 0.6176285743713379], [0.5388152003288269, 0.6069222688674927], [0.5284467339515686, 0.823788583278656], [0.5362531542778015, 0.8100944757461548], [0.5220070481300354, 0.8764268159866333], [0.5246973633766174, 0.8620489239692688], [0.5149024128913879, 0.8753319978713989], [0.5249133110046387, 0.8702012896537781], [0.5180943012237549, 0.8603499531745911], [0.5282599925994873, 0.8534661531448364], [0.6579269170761108, 0.13461680710315704], [0.6578527688980103, 0.1258750706911087], [0.676196813583374, 0.48177868127822876], [0.6713148355484009, 0.4723410904407501], [0.6760625839233398, 0.8309071660041809], [0.6722913980484009, 0.8086751103401184], [0.6971592307090759, 0.8939860463142395], [0.6910368204116821, 0.8784897923469543], [0.6030466556549072, 0.9108464121818542], [0.6014533638954163, 0.8839357495307922]]
Tadasanalandmarks = [[0.410490483045578, 0.2328002154827118], [0.4280650019645691, 0.22159677743911743], [0.4320535361766815, 0.221693217754364], [0.43611276149749756, 0.22190752625465393], [0.42749714851379395, 0.22206130623817444], [0.4308116137981415, 0.22231481969356537], [0.43426617980003357, 0.22250576317310333], [0.4647916853427887, 0.23227261006832123], [0.46034637093544006, 0.23154471814632416], [0.4216878414154053, 0.24463890492916107], [0.41975775361061096, 0.24534425139427185], [0.49513229727745056, 0.28479307889938354], [0.4942648410797119, 0.3000587224960327], [0.5183904767036438, 0.183502197265625], [0.49687495827674866, 0.20460352301597595], [0.5711736679077148, 0.09527646750211716], [0.5612694025039673, 0.11427071690559387], [0.5764906406402588, 0.07881402969360352], [0.5718562006950378, 0.10171264410018921], [0.5835961699485779, 0.080573171377182], [0.5748605728149414, 0.09858423471450806], [0.5825920701026917, 0.08578416705131531], [0.5709159970283508, 0.10452726483345032], [0.48065027594566345, 0.4892370104789734], [0.48122015595436096, 0.489828884601593], [0.48221778869628906, 0.6552572846412659], [0.4820619225502014, 0.6495009660720825], [0.5116431713104248, 0.8039002418518066], [0.511013388633728, 0.7889598608016968], [0.5362033247947693, 0.8204825520515442], [0.534211277961731, 0.8058775067329407], [0.45639100670814514, 0.8595074415206909], [0.4617781937122345, 0.8480066061019897]]




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

# def UttanasanaCheck(input_landmarks):
#     if len(input_landmarks)>0:
#             #knee_angle = angle(input_landmarks[24], input_landmarks[26], input_landmarks[28])
#             # print(knee_angle)
#             wrong_joints = poseEqualityDetector.get_wrong_joints(Uttanasanalandmarks, input_landmarks, 20)
#             if len(wrong_joints):
#                 for i in wrong_joints:
#                     print(i, wrong_joints[i])
#                 # if knee_angle > 150:
#                 #     text = "You are doing great baby!!"
#                 #     # print(f'You are doing right asana perfectly your knee angle is {knee_angle}.')
#                 #     threading.Thread(target=text_to_speech, args=(text,)).start()
#                 # else:
#                 #     text = "You are doing the right asana, keep your legs straight,  and your knee angle is" + knee_angle + "degrees."
#                 #     # print(f'You are doing the right asana, keep your legs straight,  and your knee angle is {knee_angle}.')
#                 #     threading.Thread(target=text_to_speech, args=(text,)).start()
#             else:
#                 text = "Your are doing it correct."
#                 # print("Your are doing the wrong asana.")
#                 threading.Thread(target=text_to_speech, args=(text,)).start()

# def TadasanaCheck(input_landmarks):
#     if len(input_landmarks)>0:
#             knee_angle = angle(input_landmarks[24], input_landmarks[26], input_landmarks[28])
            
#             elbow_angle = angle(input_landmarks[12], input_landmarks[14], input_landmarks[16])
#             # print(f'knee_angle: {knee_angle}, elbow_angle: {elbow_angle}')
#             # print(f'left_heel: {input_landmarks[30][1]}, left_foot_index: {input_landmarks[32][1]}')
#             if PoseSimilarity.compare_poses(Tadasanalandmarks, input_landmarks):
#                 # text = "You are doing right asana."
#                 if(knee_angle < 165):
#                     text ="Please keep your knee straight." 
                    
#                 elif(elbow_angle < 165):
#                     text = "Please keep your elbow straight up."
#                     # print("Please keep your elbow straight.")
#                 elif ((abs(input_landmarks[30][1] - input_landmarks[32][1]))<0.01):
#                     text = "Please try to stand on your toes."
#                     # print("Please try to stand on your toes.")
#                 else:
#                     text = "You are doing great baby"
#                     # print("You are doing great baby!!")
#                 threading.Thread(target=text_to_speech, args=(text,)).start()
#             else:
#                 text = "You are doing wrong asana."
#                 # print("Your are doing the wrong asana.")
#                 if(knee_angle < 165):
#                     text ="Please keep your knee straight." 
                    
#                 elif(elbow_angle < 165):
#                     text = "Please keep your elbow straight."
#                     # print("Please keep your elbow straight.")
#                 elif ((abs(input_landmarks[30][1] - input_landmarks[32][1]))<0.01):
#                     text = "Please try to stand on your toes."
#                     # print("Please try to stand on your toes.")
#                 threading.Thread(target=text_to_speech, args=(text,)).start()

# threading.Thread(target=text_to_speech, args=("Keep going!",)).start()
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

        current_time = time.time()
        pose_name = "pranamasana"
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
                
                

        # ctime = time.time()
        # fps = 1/(ctime-ptime)
        # ptime = ctime
        # cv.putText(input_frame, str(f'{int(fps)} FPS'), (30, 40), cv.FONT_HERSHEY_PLAIN, 1.7, (0,255,0), thickness=3)
        # webImg = cv.cvtColor(input_frame, cv.COLOR_BGR2RGB)
        # img_placeholder.image(webImg, caption="MYImage")

        
         
        cv.imshow('Video', input_frame)

        if cv.waitKey(10) and 0xFF == ord('q'):
            break
        # cv.waitKey(10)
cv.destroyAllWindows()