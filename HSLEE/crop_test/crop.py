import cv2
import sys
import mediapipe as mp
import math
import numpy as np
import time

mp_pose = mp.solutions.pose

file_path = 'videos/' + sys.argv[1]

extract_time_by_per_frame = 1 # 6프레임당 1프레임 저장 (보통 24fps 또는 30fps 이므로 최대공약수 이용)
frame_counter = 0
frame_number = 1




###################### image #######################

# image = cv2.imread(file_path)
#
# width = image.shape[1]
# height = image.shape[0]
# scale = 0.00392
#
# classes = None
#
# with open("coco.names", 'r') as f:
#     classes = [line.strip() for line in f.readlines()]
#
# COLORS = np.random.uniform(0, 255, size=(len(classes), 3))
# net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
# layer_names = net.getLayerNames()
# output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
#
# blob = cv2.dnn.blobFromImage(image, scale, (416, 416), (0, 0, 0), True, crop=False)
# net.setInput(blob)
# outs = net.forward(output_layers)
#
# outputs = []
#
# person_number = 1
# same_check_x = -50.0
#
# for out in outs:
#     for detection in out:
#         image2 = image
#         scores = detection[5:]
#         class_id = np.argmax(scores)
#         confidence = scores[class_id]
#         if confidence > 0.9 and str(classes[class_id]) == "person":
#             center_x = int(detection[0] * width)
#             center_y = int(detection[1] * height)
#             w = int(detection[2] * width)
#             h = int(detection[3] * height)
#             x = center_x - w / 2
#             y = center_y - h / 2
#
#             if x >= 20:
#                 x = x - 20
#             else:
#                 x = 0
#
#             if y >= 20:
#                 y = y - 20
#             else:
#                 y = 0
#
#             w, h = w + 20, h + 20
#
#             if(same_check_x - 45.0 < x and x <= same_check_x + 45.0):
#                 print("same person")
#                 continue
#             else:
#                 same_check_x = x
#                 print("x : " + str(x) + ", y : " + str(y) + ", w : " + str(w) + ", h : " + str(h) + ", confidence : " + str(confidence) + "\n")
#                 crop_img = image2[math.floor(y):math.ceil(y + h), math.floor(x):math.ceil(x + w)]
#                 cv2.imwrite("crop/frame" + str(frame_number) + "_" + str(person_number) + ".jpg", crop_img)
#                 outputs.append(crop_img)
#                 person_number += 1




###################### video #######################

start_time = time.time()

cap = cv2.VideoCapture(file_path)

while cap.isOpened():
    success, frame = cap.read()
    frame_counter += 1 #increase frame counter

    if not success:
        print("No frame.")
        # If loading a video, use 'break' instead of 'continue'.
        break

    if success:
        if frame_counter % extract_time_by_per_frame == 0:
            width = frame.shape[1]
            height = frame.shape[0]

            # 필요해서 그대로 복붙한 것
            scale = 0.00392
            classes = None

            with open("coco.names", 'r') as f:
                classes = [line.strip() for line in f.readlines()]

            COLORS = np.random.uniform(0, 255, size=(len(classes), 3))
            net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
            layer_names = net.getLayerNames()
            output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

            blob = cv2.dnn.blobFromImage(frame, scale, (416, 416), (0, 0, 0), True, crop=False)
            net.setInput(blob)
            outs = net.forward(output_layers)

            outputs = []

            person_number = 1 # 크롭된 이미지 번호 출력하기 위함
            same_check_x = -50.0
            person1_flag = False
            person2_flag = False
            next_frame_flag = False

            for out in outs:
                if next_frame_flag == True:
                    break

                person1_flag = True
                for detection in out:
                    if person1_flag == True and person2_flag == True:
                        next_frame_flag = True
                        break

                    image2 = frame
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.9 and str(classes[class_id]) == "person":
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)
                        x = center_x - w / 2
                        y = center_y - h / 2

                        if x >= 20:
                            x = x - 20
                        else:
                            x = 0

                        if y >= 20:
                            y = y - 20
                        else:
                            y = 0

                        w, h = w + 20, h + 20

                        if (same_check_x - 45.0 < x and x <= same_check_x + 45.0):
                            print("same person")
                            continue
                        else:
                            same_check_x = x
                            print("x : " + str(x) + ", y : " + str(y) + ", w : " + str(w) + ", h : " + str(
                                h) + ", confidence : " + str(confidence) + "\n")
                            crop_img = image2[math.floor(y):math.ceil(y + h), math.floor(x):math.ceil(x + w)]
                            cv2.imwrite("crop/frame" + str(frame_number) + "_" + str(person_number) + ".jpg", crop_img)
                            outputs.append(crop_img)
                            person_number += 1

                        if person_number == 3:
                            person2_flag = True

            frame_number += 1
            print("----------------------------- \n\n")

print("Elapsed time : ", time.time() - start_time)