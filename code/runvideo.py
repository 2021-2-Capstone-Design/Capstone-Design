import vlc
import time
"""
def run_video():
    media_player = vlc.MediaPlayer()
    media_file = 'sample_dance/videoplayback.mp4'
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
"""
# vlc media player 객체 생성
media_player = vlc.MediaPlayer()
 
# 뮤직비디오 파일
media_file = "BTS Dynamite MV.mp4"
 
# 미디어 파일을 vlc 객체로 읽어들이기
media = vlc.Media(media_file)
 
# 읽어드린 미디어파일을 media_player 객체에 세팅하기(재생목록)
media_player.set_media(media)
 
# 영상 스케일 조정하기
media_player.video_set_scale(0.6)
time.sleep(1)
print(f"(0) 영상스케일을 {media_player.video_get_scale()}으로 초기 조정")
 
# 볼륨 조정하기
media_player.audio_set_volume(80)
time.sleep(1)
print(f"(0) 오디오 볼륨을 {media_player.audio_get_volume()}으로 초기 조정")
 
# play() 호출이후 time.sleep을 호출하는 이유는
# python-vlc의 재생은 비동기적으로 처리되기 때문에
# 프로그램이 종료되면 영상도 바로 종료되어 테스트 결과를 볼 수 없습니다.
# 따라서 영상길이와 상관없이 5초 동안 영상을 플레이 시키기 위해
# sleep을 걸어줍니다.
print(f"(0) 초기 재생상태(get_state): {media_player.get_state()}")
print("\n")
 
print("(1) 영상 재생 시작")
media_player.play()
time.sleep(3)
print(f" - 재생중 상태 체크값(is_playing): {media_player.is_playing()}")
print("\n")
 
print("(2) 영상을 1초 일시 중지")
media_player.pause()
time.sleep(3)
print(f"- 현재 play 상태(get_state): {media_player.get_state()}")
print("\n")
 
print("(3) 영상을 1초 동안 재생")
media_player.play()
time.sleep(3)
print(f"  - 현재 play 상태(get_state): {media_player.get_state()}")
print("\n")
 
 
print("(4) 영상 재생을 중지")
media_player.stop()
time.sleep(1)
print(f"  - 현재 play 상태(get_state): {media_player.get_state()}")
print("\n")
 
print("(5) 영상을 다시 재생")
media_player.play()
time.sleep(3)
print(f"  - 현재 play 상태(get_state): {media_player.get_state()}")
print("\n")
 
 
print("(6) 영상을 30% 앞으로 이동시킵니다.")
# 0~1 사이의 비율(%)값을 인자로 넣습니다.
media_player.set_position(0.3)
time.sleep(3)
print(f"  - 영상 재생시간: {media_player.get_time()}")
print(f"  - 영상 재생위치: {media_player.get_position()}")
print("\n")
 
print("(7) 재생속도를 1.5배속으로 조정합니다.")
# 배속의 정수 값을 가집니다.
media_player.set_rate(1.5)
time.sleep(3)
print(f"  - 현재 재생 속도: {media_player.get_rate()}")
print("\n")
 
 
print("(8) 재생속도를 1배속으로 다시 조정합니다.")
# 배속의 정수 값을 가집니다.
media_player.set_rate(1)
time.sleep(3)
print(f"  - 현재 재생 속도: {media_player.get_rate()}")
print("\n")
 
print("(9) 오디오 음소거를 합니다.")
media_player.audio_toggle_mute()
time.sleep(3)
value = media_player.audio_get_mute()
print(f"  - 현재 음소거 상태: {value}")
print("\n")
 
 
print("(10) 오디오 음소거 다시 원위치 합니다.")
media_player.audio_toggle_mute()
time.sleep(3)
value = media_player.audio_get_mute()
print(f"  - 현재 음소거 상태: {value}")
print("\n")
 
 
print("(11) 화면을 Full screen으로 바꿔줍니다")
# 영상비율도 같이 바꿔줘야 합니다.
media_player.video_set_scale(2)
media_player.set_fullscreen(True)
time.sleep(3)
print("  - 현재 Full screen 상태(get_fullscreen): ", media_player.get_fullscreen())
print("\n")
 
print("(12) Full screen 토글")
# 영상비율도 같이 바꿔줘야 합니다.
media_player.video_set_scale(0.6)
media_player.toggle_fullscreen()
time.sleep(3)
print("  - 현재 Full screen 상태(get_fullscreen): ", media_player.get_fullscreen())
print("\n")