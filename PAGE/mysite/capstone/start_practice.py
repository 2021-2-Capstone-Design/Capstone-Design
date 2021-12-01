import sys
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
import tkinter as tk


# start_practice
vlc_play_flag = False
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.destroy()
record_flag = 1
video_start_flag = 0
dance_name = 'person_back' #sys.argv[1]
record_video_path = 'capstone/record_videos/' + dance_name + '_record.mp4' 
video_path = 'capstone/videos/' + dance_name + '.mp4'
show_webcam_flag = 1 # int(sys.argv[2]) #웹캠 보여주는 flag
flag = 0

def run_video():
    global record_flag
    global video_start_flag
    media_player = vlc.MediaPlayer()
    media_file = video_path
    media = vlc.Media(media_file)
    media_player.set_media(media)
    media_player.video_set_scale(1)
    media_player.audio_set_volume(100)
    media_player.set_fullscreen(True)

    time.sleep(9)
    # while True:
    #     if vlc_play_flag == True:
    #         break
    media_player.play()
    time.sleep(1)
    video_runtime = media_player.get_length()
    time.sleep(video_runtime/1000)
    media_player.stop()
    record_flag = 0
    return

def record_video_with_webcam_window():
    global vlc_play_flag, flag
    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    webcam = cv2.VideoCapture(0)
    webcam.set(3,640)
    webcam.set(4,360)
    width = int(webcam.get(3))
    height = int(webcam.get(4))
    fcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(record_video_path, fcc, fps, (width, height), True)
    while webcam.isOpened():
        vlc_play_flag = True
        if record_flag == 1:
            success, img = webcam.read()
            #imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.flip(img,1)
            out.write(img)
        else:
            out.release()
            webcam.release()
            cv2.destroyAllWindows()
            break
        cv2.putText(img, 'recording',(10,10),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),2,cv2.LINE_AA) #recording 표시
        cv2.imshow('Webcam', img)
        cv2.setWindowProperty('Webcam', cv2.WND_PROP_TOPMOST, 1)
        cv2.resizeWindow("Webcam", 320, 180)
        cv2.moveWindow('Webcam', screen_width - 320, screen_height - 180)
        if cv2.waitKey(1) & 0xFF == 27:
            out.release()
            cv2.destroyAllWindows()
            break
    out.release()
    webcam.release()
    cv2.destroyAllWindows()
    flag = 1

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
    out.release()
    webcam.release()
    cv2.destroyAllWindows()


# if show_webcam_flag == 1:
#     threading.Thread(target = record_video_with_webcam_window).start()
#     threading.Thread(target = run_video).start()
# else:
#     threading.Thread(target = record_video_without_webcam_window).start()
#     threading.Thread(target = run_video).start()

def start_practice_main(songname):
    global dance_name, record_video_path, video_path, flag
    dance_name = songname
    record_video_path = 'capstone/record_videos/' + dance_name + '_record.mp4' 
    video_path = 'capstone/videos/' + dance_name + '.mp4'

    if show_webcam_flag == 1:
        threading.Thread(target = record_video_with_webcam_window).start()
        threading.Thread(target = run_video).start()
    else:
        threading.Thread(target = record_video_without_webcam_window).start()
        threading.Thread(target = run_video).start()

    # while True:
    #     if flag == 1:
    #         return True

    # return render(request,'capstone/mainpage.html')
