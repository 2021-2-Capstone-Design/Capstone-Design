import vlc
import time

def stop_and_go():
    media_player = vlc.MediaPlayer()
    media_file = './../../sample_dance/videoplayback.mp4'
    media = vlc.Media(media_player)
    media_player.play()
    time.sleep(0.1)
    video_runtime = media_player.get_length()
    time.sleep(0.1)
    media_player.pause()
    time.sleep(2)
    media_player.resume()
    time.sleep(video_runtime/1000)
    media_player.stop()
    return

stop_and_go()