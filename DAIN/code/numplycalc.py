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



# step 1 end


###start step2 --> 영상 추출
# extract_file = open('./DAIN/extractsamples/result.txt','w')
cap = cv2.VideoCapture('./sample_dance/videoplayback.mp4') 
fps = cap.get(cv2.CAP_PROP_FPS)

#control frame rate
frame_counter = 0
frameTime = int((1/fps)*1000)  #time of each frame (ms단위, 몇ms당 1frame으로 할지 설정)
print(fps)
extract_time_by_per_frame = 1 #몇프레임 당 한번 측정할지 조절 가능

result = [] # 추출된 영상의 전체 넘파이 배열

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
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

    cap.release()
    cv2.destroyAllWindows()
    # extract_file.close()


print('*****extract success*****')
z = result.shape[0]/(33*3)
result = np.reshape(result,(int(z),33,3)) # frame 수,  tracking좌표 수, xyz 
print(result[0])
print(result.shape)


# body index
body_index = [
    [11,13,15], # left arm
    [12,14,15], # right arm
    [23,25,27], # left leg
    [24,26,28],#right leg
]
l1 = result[0][11]
l2 = result[0][13]
l3 = result[0][15]


ll1 = l1-l2
ll2 = l3-l2

innerAB = np.dot(ll1,ll2)
AB = np.linalg.norm(ll1) * np.linalg.norm(ll2)
angle = np.arccos(innerAB/AB)
print(angle)
print(angle/np.pi*180)



# for num, r in enumerate(result):
#     print(num,r)




