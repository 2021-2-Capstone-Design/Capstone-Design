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
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

###gesture list
def dist(x1,y1,x2,y2): # 비교를 위한 거리 계산 함수
    return math.sqrt( math.pow(x1-x2,2) + math.pow(y1-y2,2))

compareIndex = [[18,4],[6,8],[10,12],[14,16],[18,20]] # 마디 index 번호
hand_open = [False,False,False,False,False] # False로 초기화
gesture = [
    [False,True,True,False,False,"Yeah"],
    [True,False,False,False,False,"Good"],
]

##mediapipe tools
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mpHands = mp.solutions.hands
my_hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

def wait_gesture():
    count = 0
    cap = cv2.VideoCapture(0)
    ifExit = False
    cap.set(3, 1024)  # 16:9비율
    cap.set(4, 576)
    while cap.isOpened():
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = my_hands.process(imgRGB)
        if not success:
            print("Ignoring empty camera frame.")
            continue

        if results.multi_hand_landmarks:
            for handLandmark in results.multi_hand_landmarks:
                if (count > 60): break

                for i in range(0, 5):  # 모든 손가락 확인
                    if (count > 60): break
                    hand_open[i] = (dist(handLandmark.landmark[0].x, handLandmark.landmark[0].y,
                                         handLandmark.landmark[compareIndex[i][0]].x,
                                         handLandmark.landmark[compareIndex[i][0]].y)) < (
                                       dist(handLandmark.landmark[0].x, handLandmark.landmark[0].y,
                                            handLandmark.landmark[compareIndex[i][1]].x,
                                            handLandmark.landmark[compareIndex[i][1]].y))

                # gesture 배열에 있는 손동작과 같은지 확인하기
                for i in range(0, len(gesture)):
                    if (count > 60): break
                    flag = True
                    for j in range(0, 5):
                        if (gesture[i][j] != hand_open[j]):
                            flag = False
                    if (flag == True):
                        if (gesture[i][5] == "Good"):
                            count += 1
                            break
                mpDraw.draw_landmarks(img, handLandmark, mpHands.HAND_CONNECTIONS)
        print(count)
        cv2.imshow('MediaPipe Hands', cv2.flip(img, 1))  # 셀프 카메라이므로 좌우반전 돼서 나오게
        if cv2.waitKey(1) & 0xFF == 27:
            break
        if count > 60:
            break
    cap.release()
    cv2.destroyAllWindows()


def wait_gesture_main(request):
    render(request, 'capstone/waiting.html')
    wait_gesture()
    return render(request, 'capstone/practice.html')