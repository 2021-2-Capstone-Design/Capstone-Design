import cv2
import os
import mediapipe as mp
import math
import numpy as np
import sys
from time import sleep
from django.shortcuts import render

dance_name = "" # sys.argv[1]
select_person = "" # sys.argv[2]
saving_path = ""
path = ""
flag = 0

mp_pose = mp.solutions.pose

def video_extract():
    file_index = 1
    txt = open(saving_path, 'w')

    frame_counter = 0
    extract_time_by_per_frame = 2

    while True:
        file = str(file_index) + '.jpg'
        if file in os.listdir(path):
            file_name = path + file
            frame = cv2.imread(file_name)

            result = np.array([])
            bone_index = [11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28]

            with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
                frame_counter += 1  # increase frame counter

                if frame_counter % extract_time_by_per_frame == 0:
                    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    image.flags.writeable = False

                    # Detection
                    results = pose.process(image)

                    # Recolor image RGB to BGR
                    image.flags.writeable = True
                    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


                    # Extract landmarks
                    try:  # success to extract landmarks
                        landmarks = results.pose_landmarks.landmark

                        ret = []

                        # # 11 12 13 14 15 16 23 24 25 26 27 28
                        for i in bone_index:
                            temp = np.array([landmarks[i].x, landmarks[i].y, landmarks[i].z], float)
                            ret = np.append(ret, temp, axis=0)

                        for j in range(len(ret)):
                            txt.write(str(ret[j]))
                            if (j != len(ret) - 1):
                                txt.write(" ")
                            else:
                                pass

                        txt.write("\n")

                        result = np.append(result, ret, axis=0)
                    except:
                        pass

            if cv2.waitKey(1) & 0xFF == 27:
                break
        else:
            break
        file_index += 1
    txt.close()
    cv2.destroyAllWindows()
    # extract_file.close()

    print('*****extract success*****')

def extract_multiperson_main(songname, num): #여기 변수 두개 받아와요 ㅜㅜ 이거를 songname하고 num을 합쳐서 하나로 받아와서 자르던지..? 뭐 해야할듯..
    global dance_name, select_person, path, saving_path, flag
    flag = 0

    dance_name = songname
    select_person = num
    saving_path = "capstone/original_coordinate/" + dance_name + ".txt"


    if select_person == 1:
        path = 'capstone/crop/' + dance_name + '_1/'  # user input multiperson
          # user joint coordinate
    elif select_person == 2:
        path = 'capstone/crop/' + dance_name + '_2/'
        
    print(saving_path)
    video_extract()
    flag = 1
    # 이 부분부터 start_practice2 로 연결
    # return render(request, 'capstone/practice.html')