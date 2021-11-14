import cv2
import mediapipe as mp
import math
import numpy as np
from time import sleep
from ffpyplayer.player import MediaPlayer
from mediapipe.python.solutions import hands

###gesture list
def dist(x1,y1,x2,y2): # 비교를 위한 거리 계산 함수
    return math.sqrt( math.pow(x1-x2,2) + math.pow(y1-y2,2))

compareIndex = [[18,4],[6,8],[10,12],[14,16],[18,20]] # 마디 index 번호
hand_open = [False,False,False,False,False] # False로 초기화
gesture = [
    [False,True,True,False,False,"Yeah"],
    [True,False,False,False,False,"Good"],
]
###end gesture list

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mpHands = mp.solutions.hands
my_hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils






# step0 --> 영상 추출
video = cv2.VideoCapture('./sample_dance/videoplayback.mp4') 
fps = video.get(cv2.CAP_PROP_FPS)

#control frame rate
frame_counter = 0
frameTime = int((1/fps)*1000)  #time of each frame (ms단위, 몇ms당 1frame으로 할지 설정)
print(fps)
extract_time_by_per_frame = 1 #몇프레임 당 한번 측정할지 조절 가능

result = [] # 추출된 영상의 전체 넘파이 배열

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while video.isOpened():
        ret, frame = video.read()
        frame_counter += 1 #increase frame counter

        #Recolor image to RGB
        if ret:
            if frame_counter % extract_time_by_per_frame == 0:
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False

                #Detection
                results = pose.process(image)

                #Recolor image RGB to BGR
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                #Extract landmarks
                try: #success to extract landmarks
                    landmarks = results.pose_landmarks.landmark
                    
                    ret = []
                    for i in range(len(landmarks)):
                        
                        temp = np.array([landmarks[i].x,landmarks[i].y,landmarks[i].z], float)
                        ret = np.append(ret,temp,axis = 0)
                    
                    #print(ret)
                    result = np.append(result,ret,axis=0)
                except:
                    pass
        
        else: #no next frame (end point of video)
            break
            #Show video on screen
        cv2.imshow('dance_file',frame)
        
        if cv2.waitKey(frameTime) & 0xFF == 27:
            break

    video.release()
    cv2.destroyAllWindows()
    # extract_file.close()


print('*****extract success*****')
z = result.shape[0]/(33*3)
result = np.reshape(result,(int(z),33,3)) # frame 수,  tracking좌표 수, xyz 
print(result[0])
print(result.shape)




# 그 다음 steps

cap = cv2.VideoCapture(0) # camera
ifExit = False #yeah 손동작 인식했는지 필요없음

step = 1
while cap.isOpened():
    success,img = cap.read() # read videocapture
    #h,w,c = img.shape # x, y, z 
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = my_hands.process(imgRGB)
    if not success:
        print("Ignoring empty camera frame.")
        continue


    if (step == 1): # 따봉 제스쳐 인식
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
                            step = 2

                mpDraw.draw_landmarks(img,handLandmark,mpHands.HAND_CONNECTIONS)
                # flag = True
                # for i in range(0,5): # 손동작 맞는지 파악
                #     if(gesture[i]!=hand_open[i]):
                #         flag = False # 하나라도 틀리면 False
                # if(flag == True): ifExit = True
                
    elif (step == 2):
        print("step 2")    
        #break 








    cv2.imshow('MediaPipe Hands', cv2.flip(img, 1)) # 셀프 카메라이므로 좌우반전 돼서 나오게
    if cv2.waitKey(5) & 0xFF == 27:
        break
print("hand end")

print("end")


