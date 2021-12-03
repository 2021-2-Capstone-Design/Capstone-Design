
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse
from .models import *

from subprocess import run, PIPE
import sys
app_name = 'capstone'


def main(request):
    # return render(request, 'capstone/test1.py')
    return render(request, 'capstone/demo_intro.html')


def demo_intro(request):
    # return HttpResponse("Hello world")
    return render(request, 'capstone/demo_intro.html')

def practice(request):
    # return HttpResponse("Hello world")
    return render(request, 'capstone/practice.html')


def demo_practice(request):
    song_list = DanceInfo.objects.order_by('song')

    # return HttpResponse("Hello world")
    return render(request, 'capstone/demo_practice.html', context={'song_list': song_list})

def demo_upload(request):
    # return HttpResponse("Hello world")
    return render(request, 'capstone/demo_upload.html')

def demo_history(request):
    record_list = Record.objects.order_by() # Team.objects.all()
    # return HttpResponse("Hello world")
    return render(request, 'capstone/demo_history.html',{'record_list': record_list})

def demo_extract(request):
    # return HttpResponse("Hello world")
    return render(request, 'capstone/demo_extract.html')

def demo_film(request):
    # return HttpResponse("Hello world")
    return render(request, 'capstone/demo_film.html')

def demo_score(request, songname):
    # return HttpResponse("Hello world")
    return render(request, 'capstone/demo_score.html')


def team(request):
    team_list = Team.objects.order_by('teamName') # Team.objects.all()
    context = {'team_list': team_list}
    return render(request, 'capstone/team.html', context)
    # return render(request, 'capstone/team.html')


def songlist(request):
    song_list = DanceInfo.objects.order_by('song')
    context = {'song_list': song_list}
    return render(request, 'capstone/songlist.html', context)






def practice(request):
    song_list = DanceInfo.objects.order_by('song')
    context = {'song_list': song_list}
    # inp = request.POST.get('param')
    # out = run([sys.executable, './test1.py',inp], shell = False, stdout=PIPE)
    # print(out)

    #return render(request, 'capstone/practice.html')
    return render(request, 'capstone/practice.html', context)








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