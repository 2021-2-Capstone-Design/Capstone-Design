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


###gesture list
def dist(x1, y1, x2, y2):  # 비교를 위한 거리 계산 함수
    return math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))


compareIndex = [[18, 4], [6, 8], [10, 12], [14, 16], [18, 20]]  # 마디 index 번호
hand_open = [False, False, False, False, False]  # False로 초기화
gesture = [
    [False, True, True, False, False, "Yeah"],
    [True, False, False, False, False, "Good"],
]
###end gesture list

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mpHands = mp.solutions.hands
my_hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.destroy()
###flag, 경로 등 변수들 변경
record_flag = 1
video_start_flag = 0
estimate_start_flag = 0
saving_video_path = './../extractsamples/personback_player.mp4'
video_path = './../sample_dance/person_back.mp4'

###

def run_video():
    global record_flag
    global video_start_flag
    global estimate_start_flag
    media_player = vlc.MediaPlayer()
    media_file = video_path
    media = vlc.Media(media_file)
    media_player.set_media(media)
    media_player.video_set_scale(1)
    media_player.audio_set_volume(100)
    while True:
        if video_start_flag == 1:
            time.sleep(2)  # 따봉 인식하면 2초 있다가 영상 재생 시작
            break
    media_player.play()
    time.sleep(1)
    video_runtime = media_player.get_length()
    time.sleep(video_runtime / 1000)
    media_player.stop()
    record_flag = 0
    return 0


def gesture_savevideo():
    global video_start_flag
    global estimate_start_flag
    global video_path
    cap = cv2.VideoCapture(0)  # camera
    cap2 = cv2.VideoCapture(video_path)
    ifExit = False  # yeah 손동작 인식했는지 필요없음
    cap.set(3, 1280)
    cap.set(4, 960)
    width = int(cap.get(3))
    height = int(cap.get(4))
    step = 1
    fps = cap2.get(cv2.CAP_PROP_FPS)
    fcc = cv2.VideoWriter_fourcc(*'FMP4')
    out = cv2.VideoWriter(saving_video_path, fcc, fps, (width, height), True)
    delay = int(1000 / fps);

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

        elif (step == 2):
            if (record_flag == 1):
                print("recording...")
                out.write(img)
            else:
                print("record stop")
                estimate_start_flag = 1
                out.release()
                cv2.destroyAllWindows()
                break

        cv2.imshow('MediaPipe Hands', cv2.flip(img, 1))  # 셀프 카메라이므로 좌우반전 돼서 나오게
        cv2.moveWindow('MediaPipe Hands', screen_width // 2, 0)
        if cv2.waitKey(delay) & 0xFF == 27:
            break


def estimate_video():
    cap = cv2.VideoCapture(saving_video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(fps)
    frameTime = int((1 / fps) * 1000)
    extract_time_by_per_frame = 1
    frame_counter = 0

    txt = open('./../file_to_extract/personback_player.txt', 'w')

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            frame_counter += 1  # increase frame counter

            # Recolor image to RGB
            if ret:
                if frame_counter % extract_time_by_per_frame == 0:
                    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    image.flags.writeable = False

                    # Detection
                    results = pose.process(image)

                    # Recolor image RGB to BGR
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                    image.flags.writeable = True

                    # Extract landmarks
                    try:  # success to extract landmarks
                        landmarks = results.pose_landmarks.landmark

                        ret = []
                        for i in range(len(landmarks)):
                            temp = np.array([landmarks[i].x, landmarks[i].y, landmarks[i].z], float)
                            ret = np.append(ret, temp, axis=0)

                        # 텍스트 파일에 print(ret)
                        for j in range(len(ret)):
                            # x, y, z 좌표들이 ret에 저장되어 있으므로!
                            txt.write(str(ret[j]))
                            if (j != len(ret) - 1):
                                txt.write(" ")
                            else:
                                pass
                        # 프레임 변경시 줄바꿈
                        txt.write("\n")
                    except:
                        pass

            else:  # no next frame (end point of video)
                break
                # Show video on screen
            # cv2.imshow('dance_file',frame) #측정중일땐 굳이 영상 보여줄 필요 없을듯 주석 제거하면 영상 보여줌

            if cv2.waitKey(frameTime) & 0xFF == 27:
                break

        txt.close()
        cap.release()
        cv2.destroyAllWindows()


threading.Thread(target=gesture_savevideo).start()
threading.Thread(target=run_video).start()
while True:
    if(estimate_start_flag == 1):
        estimate_video()
        break




