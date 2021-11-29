import cv2
import mediapipe as mp
import math
import numpy as np

mp_pose = mp.solutions.pose


extract_time_by_per_frame = 6 # 6프레임당 1프레임 저장 (보통 24fps 또는 30fps 이므로 최대공약수 이용)
frame_counter = 0
frame_number = 1

cap = cv2.VideoCapture(args.image)

while cap.isOpened():
    success, frame = cap.read()
    frame_counter += 1 #increase frame counter

    if not success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        continue

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

            blob = cv2.dnn.blobFromImage(image, scale, (416, 416), (0, 0, 0), True, crop=False)
            net.setInput(blob)
            outs = net.forward(output_layers)

            outputs = []

            person_number = 1 # 크롭된 이미지 번호 출력하기 위함

            for out in outs:
                for detection in out:
                    image2 = image
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > 0.5:
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)
                        x = center_x - w / 2
                        y = center_y - h / 2

                        print("x : " + str(x) + ", y : " + str(y) + ", w : " + str(w) + ", h : " + str(h) + "\n")
                        crop_img = image2[math.floor(y):round(y + h), math.floor(x):round(x + w)]
                        cv2.imwrite("frame" + str(frame_number) + "_" + str(num) + ".jpg", crop_img)
                        outputs.append(crop_img)
                        person_number += 1

            frame_number += 1