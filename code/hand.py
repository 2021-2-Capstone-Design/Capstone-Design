import cv2
import mediapipe as mp
import math
from time import sleep

from mediapipe.python.solutions import hands



# multiwindow로 구현! 

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
my_hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

def dist(x1,y1,x2,y2): # 비교를 위한 거리 계산 함수
    return math.sqrt( math.pow(x1-x2,2) + math.pow(y1-y2,2))

compareIndex = [[18,4],[6,8],[10,12],[14,16],[18,20]] # 마디 index 번호
open = [False,False,False,False,False] # False로 초기화
gesture = [
    [False,True,True,False,False,"Yeah"],
    [True,False,False,False,False,"Good"],
    

 ]#yeah 인식하면 hand tracking 끝


ifExit = False #yeah 손동작 인식했는지
i = 0
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
                open[i] = (dist(handLandmark.landmark[0].x,handLandmark.landmark[0].y,
                    handLandmark.landmark[compareIndex[i][0]].x,handLandmark.landmark[compareIndex[i][0]].y) ) <  (dist(handLandmark.landmark[0].x,handLandmark.landmark[0].y,
                    handLandmark.landmark[compareIndex[i][1]].x,handLandmark.landmark[compareIndex[i][1]].y))
            #print(open) # 손가락 길이 판단한 결과


            # gesture 배열에 있는 손동작과 같은지 확인하기
            for i in range(0,len(gesture)):
                if(ifExit == True):break
                flag = True
                for j in range(0,5):
                    if(gesture[i][j]!=open[j]):
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
            #     if(gesture[i]!=open[i]):
            #         flag = False # 하나라도 틀리면 False
            # if(flag == True): ifExit = True
                    
            
    cv2.imshow('MediaPipe Hands', cv2.flip(img, 1)) # 셀프 카메라이므로 좌우반전 돼서 나오게
    if cv2.waitKey(5) & 0xFF == 27:
        break

#cap.release()
cv2.destroyAllWindows()



# dance practice 영상 재생 & 내 영상까지 보이게 하기
dance = cv2.VideoCapture('Rock with you(1).mp4')

#cap = cv2.VideoCapture(0)


fps = dance.get(cv2.CAP_PROP_FPS)
frameTime = int((1/fps)*1000)  #time of each frame (ms단위, 몇ms당 1frame으로 할지 설정)

while dance.isOpened() and cap.isOpened():
    ret, frame = dance.read()
    r,f  = cap.read()
    #img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # RGB 처리인데 원본 색감 그대로 할거면 안해도 될 듯
    cv2.imshow('dance practice',frame)
    cv2.imshow('dance', cv2.flip(f, 1))

    if cv2.waitKey(frameTime) & 0xFF == 27:
        break
# 작업 완료 후 해제
dance.release()
cap.release()
cv2.destroyAllWindows()
print("☆☆☆Done!☆☆☆")