import vlc
import time

def run_video():
    media_player = vlc.MediaPlayer()
    media_file = './../sample_dance/videoplayback.mp4'
    media = vlc.Media(media_file)
    media_player.set_media(media)

    media_player.video_set_scale(1)
    time.sleep(1)
    media_player.audio_set_volume(50)
    time.sleep(1)
    media_player.play()
    time.sleep(8)
    media_player.stop()

run_video()

