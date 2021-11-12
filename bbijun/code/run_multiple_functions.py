import time
import threading
import cv2
import vlc


video_path = './bbijun/sample_dance/videoplayback.mp4'
thread_flag = 0

def run_video():
    global thread_flag
    thread_flag = 0
    media_player = vlc.MediaPlayer()
    media_file = video_path
    media = vlc.Media(media_file)
    media_player.set_media(media)
    media_player.video_set_scale(1)
    time.sleep(1)
    video_runtime = media_player.get_length()
    media_player.audio_set_volume(50)
    media_player.play()
    time.sleep(video_runtime/1000)
    media_player.stop()
    thread_flag = 1
    return 0

def webcam_capture():
    global thread_flag
    webcam = cv2.VideoCapture(0)
    webcam.set(3,1920)
    webcam.set(4,1080)
    width = int(webcam.get(3))
    height = int(webcam.get(4))

    while(thread_flag!=1):
        ret, frame = webcam.read()
        cv2.imshow('userWebcam', cv2.flip(frame, 1))
        if cv2.waitKey(1) == 27:
            break
    
    webcam.release()
    cv2.destryAllWindows()
    return 0

threading.Thread(target=run_video).start()
threading.Thread(target=webcam_capture).start()