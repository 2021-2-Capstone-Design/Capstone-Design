import cv2
import sys
import os
from django.http import request
import mediapipe as mp
import math
import numpy as np
import time
from django.shortcuts import render

mp_pose = mp.solutions.pose

dance_name = "" # sys.argv[1]
file_path = "" # 'videos/' + dance_name + '.mp4'
saving_person1_path = "" # 'crop/' + dance_name + '_1/'
saving_person2_path = "" # 'crop/' + dance_name + '_2/'


extract_time_by_per_frame = 1
frame_counter = 0
frame_number = 1


def cropping():
    global frame_counter
    global frame_number

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

                scale = 0.00392
                classes = None

                with open("capstone/coco.names", 'r') as f:
                    classes = [line.strip() for line in f.readlines()]

                COLORS = np.random.uniform(0, 255, size=(len(classes), 3))
                net = cv2.dnn.readNet("capstone/yolov3.weights", "capstone/yolov3.cfg")
                layer_names = net.getLayerNames()
                output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

                blob = cv2.dnn.blobFromImage(frame, scale, (416, 416), (0, 0, 0), True, crop=False)
                net.setInput(blob)
                outs = net.forward(output_layers)

                person_number = 1 # crop image numbering
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
                                if(person_number == 1):
                                    cv2.imwrite(saving_person1_path + str(frame_number) + ".jpg", crop_img)
                                elif(person_number == 2):
                                    cv2.imwrite(saving_person2_path + str(frame_number) + ".jpg", crop_img)

                                person_number += 1

                            if person_number == 3:
                                person2_flag = True

                frame_number += 1
                print("----------------------------- \n\n")

    print("Elapsed time : ", time.time() - start_time)


def crop_main( songname):
    global dance_name, file_path, saving_person1_path, saving_person2_path

    dance_name = songname

    file_path = 'capstone/videos/' + dance_name + '.mp4'
    saving_person1_path = 'capstone/crop/' + dance_name + '_1/'
    saving_person2_path = 'capstone/crop/' + dance_name + '_2/'

    try:
        if not os.path.exists(saving_person1_path):
            os.makedirs(saving_person1_path)
    except OSError:
        print ('Already existence : ' + saving_person1_path)
    try:
        if not os.path.exists(saving_person2_path):
            os.makedirs(saving_person2_path)
    except OSError:
        print ('Already existence : ' + saving_person2_path)

    cropping()
