import cv2
import numpy as np
import mediapipe as mp
import math

def dist(x1,y1,x2,y2): # 비교를 위한 거리 계산 함수
    return math.sqrt( math.pow(x1-x2,2) + math.pow(y1-y2,2))

compareIndex = [[18,4],[6,8],[10,12],[14,16],[18,20]] # 마디 index 번호
hand_open = [False,False,False,False,False] # False로 초기화
gesture = [
    [False,True,True,False,False,"Yeah"],
    [True,False,False,False,False,"Good"],
]
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mpHands = mp.solutions.hands
my_hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

def hand_motion_save_video():
    cap = cv2.VideoCapture(0)
    ifExit = False
    i=0
    while cap.isOpened():
        if(ifExit == True):
            i+=1
            if(i>=30):
                break # 시간 조금 지나서 break
            #continue
        success,img = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue
        #h,w,c = img.shape # x, y, z 
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        results = my_hands.process(imgRGB)

        if results.multi_hand_landmarks:
            for handLandmark in results.multi_hand_landmarks:
                if(ifExit == True):break

                for i in range(0,5): # 모든 손가락 확인
                    if(ifExit == True):break
                    hand_open[i] = (dist(handLandmark.landmark[0].x,handLandmark.landmark[0].y,
                        handLandmark.landmark[compareIndex[i][0]].x,handLandmark.landmark[compareIndex[i][0]].y) ) <  (dist(handLandmark.landmark[0].x,handLandmark.landmark[0].y,
                        handLandmark.landmark[compareIndex[i][1]].x,handLandmark.landmark[compareIndex[i][1]].y))
                #print(open) # 손가락 길이 판단한 결과


                # gesture 배열에 있는 손동작과 같은지 확인하기
                for i in range(0,len(gesture)):
                    if(ifExit == True):break
                    flag = True
                    for j in range(0,5):
                        if(gesture[i][j]!=hand_open[j]):
                            flag = False
                    if(flag == True):
                        # 어떤 손동작인지 인식
                        if(gesture[i][5]=="Yeah"): 
                            pass
                            #ifExit = True
                        if(gesture[i][5]=="Good"): 
                            ifExit = True

                mpDraw.draw_landmarks(img,handLandmark,mpHands.HAND_CONNECTIONS)
                # flag = True
                # for i in range(0,5): # 손동작 맞는지 파악
                #     if(gesture[i]!=hand_open[i]):
                #         flag = False # 하나라도 틀리면 False
                # if(flag == True): ifExit = True
                        
                
        cv2.imshow('MediaPipe Hands', cv2.flip(img, 1)) # 셀프 카메라이므로 좌우반전 돼서 나오게
        if cv2.waitKey(5) & 0xFF == 27:
            break