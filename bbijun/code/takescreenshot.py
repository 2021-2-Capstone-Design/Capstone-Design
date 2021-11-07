import vlc
import time
import cv2
cap = cv2.VideoCapture('.//../sample_dance/solo.mp4')
fps = cap.get(cv2.CAP_PROP_FPS)
print(fps)
frameTime = int((1/fps))
print(frameTime)

"""
#1프레임마다 스크린샷 촬영으로 코드 변경
def take_screenshot():
    cap = cv2.VideoCapture('./../../sample_dance/solo.mp4')
    fps = cap.get(cv2.CAP_PROP_FPS)
    frameTime = int((1/fps))
    print(frameTime)
    media_player = vlc.MediaPlayer()
    media_file = './../../sample_dance/solo.mp4'
    media = vlc.Media(media_file)
    media_player.set_media(media)
    media_player.set_rate(1)
    video_runtime = media_player.get_length()
    print("video runtime : "+str(video_runtime))
    i=0
    media_player.play()
    time.sleep(0.1)
    video_runtime = media_player.get_length()
    print("video runtime : "+str(video_runtime))
    while(i<video_runtime):
        time.sleep(frameTime)
        media_player.video_take_snapshot(0,'./../screenshot',0,0)
        i+=frameTime

take_screenshot()
"""