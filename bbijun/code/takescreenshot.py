import vlc
import time

def take_screenshot():
    media_player = vlc.MediaPlayer()
    media_file = './../sample_dance/videoplayback.mp4'
    media = vlc.Media(media_file)
    media_player.set_media(media)
    media_player.set_rate(10)
    
    capture_count=8
    i=0
    media_player.play()
    time.sleep(0.1)
    while(i<capture_count):
        time.sleep(0.1)
        media_player.video_take_snapshot(0,'./../screenshot',0,0)
        i+=1

take_screenshot()