import cv2
import os
import mediapipe as mp
import math
import numpy as np
import sys
from time import sleep

dance_name = sys.argv[1]
select_person = sys.argv[2]
if select_person == "1":
    path = 'crop/' + dance_name + '_1/'  # 유저 삽입(2인 영상)
    saving_path = "original_coordinate/" + dance_name + "_1.txt"  # 유저 영상 관절 좌표
if select_person == "2":
    path = 'crop/' + dance_name + '_2/'
    saving_path = "original_coordinate/" + dance_name + "_2.txt"  # 유저 영상 관절 좌표

mp_pose = mp.solutions.pose

def video_extract():
    file_index = 1
    txt = open(saving_path, 'w')

    frame_counter = 0
    extract_time_by_per_frame = 2  # 몇프레임 당 한번 측정할지 조절 가능

    while True:
        file = str(file_index) + '.jpg'
        if file in os.listdir(path):
            file_name = path + file
            frame = cv2.imread(file_name)

            # frameTime = int((1/fps)*1000)  #time of each frame (ms단위, 몇ms당 1frame으로 할지 설정)

            result = np.array([])  # 추출된 영상의 전체 넘파이 배열
            bone_index = [11, 12, 13, 14, 15, 16, 23, 24, 25, 26, 27, 28]  # 필요한 관절 번호

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
                        for i in bone_index:  # 필요한 부분의 관절의 정보만
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

video_extract()

# def extract_record_video_main(request):
#     video_extract()
#     return render(request, 'capstone/practice.html')