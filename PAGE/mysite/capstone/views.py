
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse
from .models import *

from subprocess import run, PIPE
import sys
app_name = 'capstone'


def main(request):
    # return render(request, 'capstone/test1.py')
    return render(request, 'capstone/mainpage.html')


def first(request):
    # return HttpResponse("Hello world")
    return render(request, 'capstone/firstpage.html')


def team(request):
    team_list = Team.objects.order_by('teamName') # Team.objects.all()
    context = {'team_list': team_list}
    return render(request, 'capstone/team.html', context)
    # return render(request, 'capstone/team.html')


def songlist(request):
    song_list = DanceInfo.objects.order_by('song')
    context = {'song_list': song_list}
    return render(request, 'capstone/songlist.html', context)






def  practice(request):
    song_list = DanceInfo.objects.order_by('song')
    context = {'song_list': song_list}
    # inp = request.POST.get('param')
    # out = run([sys.executable, './test1.py',inp], shell = False, stdout=PIPE)
    # print(out)

    #return render(request, 'capstone/practice.html')
    return render(request, 'capstone/practice.html', context)


def practice_detail(request, songname):
    aa = str(songname)
    #return HttpResponse( songname)
    return render (request, 'capstone/practice_song.html', {'song' : songname})

def step1(request, songname):
    aa = str(songname)
    #return HttpResponse( songname)
    return render (request, 'capstone/step1.html', {'song' : songname})

def step2(request, songname):
    aa = str(songname)
    #return HttpResponse( songname)
    return render (request, 'capstone/step2.html', {'song' : songname})

def step3(request, songname):
    aa = str(songname)
    # return HttpResponse( songname)
    return render (request, 'capstone/step3.html', {'song' : songname})





def record(request):
    return render(request, 'capstone/record.html')


def mypage(request):
    return render(request, 'capstone/mypage.html')


def waiting(request):
    return render(request, 'capstone/waiting.html')

# if __name__ = "__main__":
#     print('main')

# def main(request):
#     return mypage(request)