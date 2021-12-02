from django.shortcuts import render

from . import start_practice
from . import extract_record_video
from . import load_score
from . import start_practice2
from . import extract_to_calculate
from . import crop
from . import extract_upload_video
from . import extract_multiperson

import math


# 이미 db에 있는 영상일 때의 steps


# 노래를 선택하면 노래에 대한 정보(?)를 보여주는 페이지
def practice_detail(request, songname):
  #return HttpResponse( songname)
  return render (request, 'capstone/practice_song.html', {'song' : songname, })

def step1main(request, songname):
  start_practice2.start_practice2_main(songname)
  return render (request, 'capstone/step1.html', {'song' : songname})


def step2main(request, songname):
  print("step2" + songname)
  
  score = math.ceil(extract_to_calculate.extract_to_calculate_main(songname))
  return render (request, 'capstone/demo_score.html', {'song' : songname, 'score' : score})
  #extract_record_video.extract_record_video_main(songname)
  #load_score.load_score_main(songname)
  

def step3main(request, songname):
  #start_practice.start_practice_main(songname)
  #dir = 'capstone/' + songname + '/step1/'
  return render (request, 'capstone/step3.html', {'song' : songname})


# 사용자가 업로드 했을 때의 과정

# 사용자 업로드--> 2인을 선택 했을 경우 해당 영상을 크롭

# 크롭
def cropping(request, songname):
  crop.crop_main(songname)
  #extract_upload_video.extract_upload_video_main(songname)
  while crop.flag == 0:
    if crop.flag == 1:
      break
  return render (request, 'capstone/demo_extract.html', {'song' : songname, })

# 사람1인지 사람2인지
def extract(request, songname, num):
  print("extract")
  #crop.crop_main(songname)
  extract_multiperson.extract_multiperson_main(songname,num)
  while extract_multiperson.flag == 0:
    if extract_multiperson.flag == 1:
      break
  start_practice2.start_practice2_main(songname)
  return render (request, 'capstone/demo_film.html', {'song' : songname, })


# 사용자 숫자 입력받는 페이지
def choosenum(request, songpath):
  songname = songpath.split('/')[-1][:-4]
  return render(request, 'capstone/demo_upload.html', {'song' : songname})


# 2인일 경우 사람1인지 사람2인지 입력받는 페이지
def chooseperson(request):
  return render(request, 'capstone/chooseperson.html')


  
def userstep1main(request, songname):
  extract_upload_video.extract_upload_video_main(songname)
  while extract_upload_video.flag == 0:
    if extract_upload_video.flag == 1:
      break
  start_practice2.start_practice2_main(songname)
  return render (request, 'capstone/demo_film.html', {'song' : songname})