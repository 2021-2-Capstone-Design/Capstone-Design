import cv2
import time

cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    