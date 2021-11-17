import cv2
import mediapipe as mp
import math
import numpy as np

mp_pose = mp.solutions.pose

# 좌표 저장할 파일
txt = open('./../file_to_extract/videoplayback_co.txt', 'w')

# 좌표 추출 코드
cap = cv2.VideoCapture('./../sample_dance/videoplayback.mp4')
fps = cap.get(cv2.CAP_PROP_FPS)

# control frame rate
frame_counter = 0
frameTime = int((1 / fps) * 1000)  # time of each frame (ms단위, 몇ms당 1frame으로 할지 설정)
print(fps)
extract_time_by_per_frame = 1  # 몇프레임 당 한번 측정할지 조절 가능

result = []  # 추출된 영상의 전체 넘파이 배열

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
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

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
                        if(j != len(ret) - 1):
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
        # cv2.imshow('dance_file', frame)

        if cv2.waitKey(frameTime) & 0xFF == 27:
            break

    cap.release()
    txt.close()
    cv2.destroyAllWindows()
    # extract_file.close()

print('*****extract success*****')






