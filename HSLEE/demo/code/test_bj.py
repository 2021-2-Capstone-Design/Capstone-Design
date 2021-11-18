import cv2
import mediapipe as mp
import math
import numpy as np
from time import sleep
from ffpyplayer.player import MediaPlayer
from mediapipe.python.solutions import hands
import time
import vlc
import threading
import imutils
import tkinter as tk


def dist(x1, y1, x2, y2):  # 비교를 위한 거리 계산 함수
    return math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))

compareIndex = [[18, 4], [6, 8], [10, 12], [14, 16], [18, 20]]  # 마디 index 번호
hand_open = [False, False, False, False, False]  # False로 초기화

# gesture list
gesture = [
    [False, True, True, False, False, "Yeah"],
    [True, False, False, False, False, "Good"],
]


# variable of MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mpHands = mp.solutions.hands
my_hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

# variable of tkinter
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.destroy()

# variable of flag and path
record_flag = 1
video_start_flag = 1
estimate_start_flag = 0
saving_video_path = './../save_user_video/user_webcam.mp4'
video_path = './../dance/solo.mp4'
cap2 = cv2.VideoCapture(video_path)
fps = cap2.get(cv2.CAP_PROP_FPS)

# Run sample.mp4 video using vlc
def run_video():
    # global variables
    global record_flag
    global video_start_flag
    global estimate_start_flag

    # vlc setting
    media_player = vlc.MediaPlayer()
    media_file = video_path
    media = vlc.Media(media_file)
    media_player.set_media(media)
    media_player.video_set_scale(1)
    media_player.audio_set_volume(100)
    media_player.set_fullscreen(True)

    # 따봉 인식하면 vlc로 영상 시작되게끔
    while True:
        if video_start_flag == 1:
            record_flag = 1
            time.sleep(7)
            break

    # vlc start
    media_player.play()
    time.sleep(1)
    video_runtime = media_player.get_length()
    time.sleep(video_runtime / 1000)
    print("stop")
    media_player.stop()

    # record finish flag
    record_flag = 0
    return 0

"""
# Save user video for extracting
def gesture_savevideo():
    # global variables
    global video_start_flag
    global estimate_start_flag
    global video_path

    # opencv
    cap = cv2.VideoCapture(0)  # camera
    cap2 = cv2.VideoCapture(saving_video_path)
    ifExit = False  # yeah 손동작 인식했는지 필요없음

    fps = cap2.get(cv2.CAP_PROP_FPS)

    # for waitKey
    # delay = int(1000 / fps)

    # step1 is checking 따봉
    step = 1
    # camera ON

    while cap.isOpened():
        success, img = cap.read()  # read videocapture
        # h,w,c = img.shape # x, y, z
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = my_hands.process(imgRGB)
        if not success:
            print("Ignoring empty camera frame.")
            continue

        if (step == 1):  # 따봉 제스쳐 인식
            if results.multi_hand_landmarks:
                for handLandmark in results.multi_hand_landmarks:
                    if (ifExit == True): break

                    for i in range(0, 5):  # 모든 손가락 확인
                        if (ifExit == True): break
                        hand_open[i] = (dist(handLandmark.landmark[0].x, handLandmark.landmark[0].y,
                                             handLandmark.landmark[compareIndex[i][0]].x,
                                             handLandmark.landmark[compareIndex[i][0]].y)) < (
                                       dist(handLandmark.landmark[0].x, handLandmark.landmark[0].y,
                                            handLandmark.landmark[compareIndex[i][1]].x,
                                            handLandmark.landmark[compareIndex[i][1]].y))
                    # print(open) # 손가락 길이 판단한 결과

                    # gesture 배열에 있는 손동작과 같은지 확인하기
                    for i in range(0, len(gesture)):
                        if (ifExit == True): break
                        flag = True
                        for j in range(0, 5):
                            if (gesture[i][j] != hand_open[j]):
                                flag = False
                        if (flag == True):
                            # 어떤 손동작인지 인식
                            if (gesture[i][5] == "Yeah"):
                                pass
                                # ifExit = True
                            if (gesture[i][5] == "Good"):
                                ifExit = True
                                step = 2
                                video_start_flag = 1

                    mpDraw.draw_landmarks(img, handLandmark, mpHands.HAND_CONNECTIONS)
                    # flag = True
                    # for i in range(0,5): # 손동작 맞는지 파악
                    #     if(gesture[i]!=hand_open[i]):
                    #         flag = False # 하나라도 틀리면 False
                    # if(flag == True): ifExit = True

        # step2 is close web camera / re open web camera for saving user video
        elif (step == 2):
            cap.release()
            cv2.destroyAllWindows()
            break

        cv2.imshow('MediaPipe Hands', cv2.flip(img, 1))  # 셀프 카메라이므로 좌우반전 돼서 나오게
        cv2.moveWindow('MediaPipe Hands', screen_width // 2, 0)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    recap = cv2.VideoCapture(0)

    # change resolution
    recap.set(3, 640)
    recap.set(4, 360)
    width = int(recap.get(3))
    height = int(recap.get(4))

    # save video in save_video folder
    fcc = cv2.VideoWriter_fourcc(*'FMP4')
    out = cv2.VideoWriter(saving_video_path, fcc, fps, (width, height), True)

    while recap.isOpened():
        ret, frame = recap.read()
        if (record_flag == 1):
            print("recording...")
            out.write(frame)
        else:
            print("record stop")
            # finish recording.
            estimate_start_flag = 1
            recap.release()
            out.release()
            break

        cv2.imshow('webcam', cv2.flip(frame, 1))
        cv2.moveWindow('webcam', screen_width // 2, 0)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cv2.destroyAllWindows()
"""
def save_video():

    recap = cv2.VideoCapture(0)
    recap.set(3, 640)
    recap.set(4, 360)
    width = int(recap.get(3))
    height = int(recap.get(4))
    fcc = cv2.VideoWriter_fourcc(*'FMP4')
    out = cv2.VideoWriter(saving_video_path, fcc, fps, (width, height), True)

    while recap.isOpened():
        ret, frame = recap.read()
        if (record_flag == 1):
            print("recording...")
            out.write(frame)
        else:
            print("record stop")
            # finish recording.
            #estimate_start_flag = 1
            recap.release()
            out.release()
            break

        cv2.imshow('webcam', cv2.flip(frame, 1))
        cv2.setWindowProperty('webcam', cv2.WND_PROP_TOPMOST, 1)
        cv2.resizeWindow('webcam', 320, 180)
        cv2.moveWindow('webcam', screen_width - 330, screen_height - 210)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cv2.destroyAllWindows()
threading.Thread(target=save_video).start()
threading.Thread(target=run_video).start()