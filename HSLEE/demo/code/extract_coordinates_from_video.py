import sys
import cv2
import mediapipe as mp

arguments = sys.argv
if len(arguments) == 1:
    print("Insert video name plz.")
    sys.exit()
else:
    file_name = arguments[1]

def extract_coordinate_from_video(saving_video_name):
    saving_video_path = './../dance/' + saving_video_name + '.mp4'
    cap = cv2.VideoCapture(saving_video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frameTime = int((1 / fps) * 1000)

    coordinate_file_path = './../coordinates/' + saving_video_name + '.txt'
    txt = open(coordinate_file_path, 'w')

    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            frame_counter += 1  # increase frame counter

            # Recolor image to RGB
            if ret:
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image.flags.writeable = False

                # Detection
                results = pose.process(image)

                # Recolor image RGB to BGR
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                image.flags.writeable = True

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
                        if (j != len(ret) - 1):
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
            # cv2.imshow('dance_file',frame) #측정중일땐 굳이 영상 보여줄 필요 없을듯 주석 제거하면 영상 보여줌

            if cv2.waitKey(frameTime) & 0xFF == 27:
                break

        txt.close()
        cap.release()
        cv2.destroyAllWindows()

extract_coordinate_from_video(file_name)