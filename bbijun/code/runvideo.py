import vlc
import time

def run_video():
    media_player = vlc.MediaPlayer()
    media_file = './../sample_dance/videoplayback.mp4'
    media = vlc.Media(media_file)
    media_player.set_media(media)
    media_player.video_set_scale(1)
    video_runtime = media_player.get_length()
    media_player.audio_set_volume(50)
    media_player.play()
    time.sleep(video_runtime/1000)
    media_player.stop()

run_video()

