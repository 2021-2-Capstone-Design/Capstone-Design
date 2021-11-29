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

##screen info
# root = tk.Tk()
# screen_width = root.winfo_screenwidth()
# screen_height = root.winfo_screenheight()
# root.destroy()

##flag, dir variables
record_flag = 1
video_start_flag = 0
# dance_name = sys.argv[1]
# record_video_path = './../record_videos/' + dance_name + '_record.mp4'
# video_path = './../videos/' + dance_name + '.mp4'
# show_webcam_flag = int(sys.argv[2]) #웹캠 보여주는 flag
# user_coordinate = './../record_coordinate/' + dance_name + '.txt'
##functions
"""
def run_video():
    global record_flag
    global video_start_flag
    media_player = vlc.MediaPlayer()
    media_file = video_path
    media = vlc.Media(media_file)
    media_player.set_media(media)
    media_player.video_set_scale(1)
    media_player.audio_set_volume(100)
    time.sleep(3)
    media_player.play()
    time.sleep(1)
    video_runtime = media_player.get_length()
    time.sleep(video_runtime/1000)
    media_player.stop()
    record_flag = 0
    return
"""


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


"""
def record_video_without_webcam_window():
    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    webcam = cv2.VideoCapture(0)
    webcam.set(3,640)
    webcam.set(4,360)
    width = int(webcam.get(3))
    height = int(webcam.get(4))
    fcc = cv2.VideoWriter_fourcc(*'FMP4')
    out = cv2.VideoWriter(record_video_path, fcc, fps, (width, height), True)
    while webcam.isOpened():
        if record_flag == 1:
            success, img = webcam.read()
            #imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.flip(img,1)
            out.write(img)
        else:
            out.release()
            cv2.destroyAllWindows()
            break
        if cv2.waitKey(1) & 0xFF == 27:
            cv2.destroyAllWindows()
            break

def record_video_with_webcam_window():
    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    webcam = cv2.VideoCapture(0)
    webcam.set(3,640)
    webcam.set(4,360)
    width = int(webcam.get(3))
    height = int(webcam.get(4))
    fcc = cv2.VideoWriter_fourcc(*'FMP4')
    out = cv2.VideoWriter(record_video_path, fcc, fps, (width, height), True)
    while webcam.isOpened():
        if record_flag == 1:
            success, img = webcam.read()
            #imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.flip(img,1)
            out.write(img)
        else:
            out.release()
            cv2.destroyAllWindows()
            break
        cv2.putText(img, 'recording',(10,10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),2,cv2.LINE_AA) #recording 표시
        cv2.imshow('Webcam', img)
        cv2.moveWindow('Webcam', screen_width-width, screen_height-height+20)
        if cv2.waitKey(1) & 0xFF == 27:
            out.release()
            cv2.destroyAllWindows()
            break

def estimate_saved_webcam():
    txt = user_coordinate
    cap = cv2.VideoCapture(record_video_path)
    extract_time_by_per_frame = 1
    frame_counter = 0
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            frame_counter += 1
            if ret:
                if frame_counter % extract_time_by_per_frame == 0:
                    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    image.flags.writeable = False
                    results = pose.process(image)
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                    image.flags.writeable = True

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
                        #end each frame
                        txt.write("\n")
                    except:
                        pass

            else:  # no next frame (end point of video)
                break
            #if cv2.waitKey(1) & 0xFF == 27: 딱히 필요 없어보임
            #    break
        txt.close()
        cap.release()
        cv2.destroyAllWindows()


wait_gesture()
if(show_webcam_flag == 1):
    threading.Thread(target = record_video_with_webcam_window).start()
    threading.Thread(target = run_video).start()
else:
    threading.Thread(target = record_video_without_webcam_window).start()
    threading.Thread(target = run_video).start()

#####여기까지 완료하고 웹으로 어떤 플레그를 줘서 '측정중입니다. 잠시 후 결과 페이지를 확인해주세요' 라는 메세지가 출력되는 웹페이지로 이동시키기
estimate_saved_webcam()

"""

def testmain(request):
    render(request, 'capstone/waiting.html')
    wait_gesture()


    #gesture_savevideo()
    # threading.Thread(target=gesture_savevideo).start()
    #threading.Thread(target=run_video).start()

    return render(request, 'capstone/practice.html')

    #return Htt