import vlc
import time
#1프레임마다 스크린샷 촬영으로 코드 변경
def take_screenshot():
    media_player = vlc.MediaPlayer()
    media_file = './../../sample_dance/solo.mp4'
    media = vlc.Media(media_file)
    media_player.set_media(media)
<<<<<<< HEAD
    media_player.set_rate(10)
    
    capture_count=120
    i=0
    media_player.play()
    time.sleep(0.1)
    while(i<capture_count):
        time.sleep(0.01)
=======
    media_player.set_rate(1)
    video_runtime = media_player.get_length()
    print("video runtime : "+str(video_runtime))
    i=0
    media_player.play()
    time.sleep(1)
    while(i<video_runtime):
        time.sleep(0.001)
>>>>>>> bbijun
        media_player.video_take_snapshot(0,'./../screenshot',0,0)
        i+=1

take_screenshot()