import cv2
import vlc
import time
import threading
import mediapipe as mp
import math
import numpy as np
from time import sleep
from mediapipe.python.solutions import hands

#####gesture list 선언
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

######옵션 설정 부분 global variable
video_path = './bbijun/sample_dance/videoplayback.mp4'  ##video경로를 넣어주세요
option_cap = cv2.VideoCapture(video_path)
fps = option_cap.get(cv2.CAP_PROP_FPS)
saving_video_path = './bbijun/extractsamples/testvideo.mp4' ##저장할 비디오의 경로를 넣어주세요
thread_flag = 0 ##영상 재생이 종료되면 촬영 영상도 끝나게 하기 위한 flag



######함수 선언 부분####
def hand_motion():
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
    cap.release()
    cv2.destroyAllWindows()


def run_video():
    global thread_flag
    thread_flag = 0
    media_player = vlc.MediaPlayer()
    media_file = video_path
    media = vlc.Media(media_file)
    media_player.set_media(media)
    media_player.video_set_scale(1)
    time.sleep(1)
    video_runtime = media_player.get_length()
    media_player.audio_set_volume(50)
    media_player.play()
    time.sleep(video_runtime/1000)
    media_player.stop()
    thread_flag = 1
    return 0

def take_video(fps):
    global thread_flag
    saving_path = saving_video_path
    saving_video = cv2.VideoCatpure(0)
    saving_video.set(3,1920)
    saving_video.set(4,1080)
    FPS = fps
    frametime = int(np.round((1/fps)*1000))
    width = int(saving_video.get(3))
    height = int(saving_video.get(4))
    fcc = cv2.VideoWriter_fourcc(*'FMP4')
    out = cv2.VideoWriter(saving_path,fcc,FPS,(width,height), True)

    while(thread_flag!=1):
        ret, frame = saving_video.read()
        cv2.imshow('user_webcam', frame)
        out.write(frame)
        if cv2.waitKey(frametime) == 27:
            break
    
    saving_video.release()
    out.release()
    cv2.destryAllWindows()



###실행부분
hand_motion()
t1 = threading.Thread(target = run_video)
t2 = threading.Thread(target = take_video)
t1.daemon = True
t2.daemon = True

t1.start()
t2.start()










