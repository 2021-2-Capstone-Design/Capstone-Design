from django.shortcuts import render

from . import start_practice
from . import extract_record_video
from . import load_score


def step1main(request, songname):
  start_practice.start_practice_main(songname)
  return render (request, 'capstone/step1.html', {'song' : songname})


def step2main(request, songname):
  extract_record_video.extract_record_video_main(songname)
  load_score.load_score_main(songname)
  return render (request, 'capstone/step2.html', {'song' : songname})




def step3main(request, songname):
  #start_practice.start_practice_main(songname)
  #dir = 'capstone/' + songname + '/step1/'
  return render (request, 'capstone/step3.html', {'song' : songname})