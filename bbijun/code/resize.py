import cv2
from time import sleep
import numpy as np
import imutils
import tkinter as tk
root = tk.Tk()
screen_width = root.winfo_screenwidth()
root.destroy()
cap = cv2.VideoCapture(0)
while cap.isOpened():
    success, img = cap.read()
    
    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    img = imutils.resize(img, width=screen_width//2)
    cv2.imshow('webcam',cv2.flip(img,1))
    cv2.moveWindow('webcam',screen_width//2,0)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cap.release()
cv2.destroyAllWindows()