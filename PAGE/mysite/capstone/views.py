
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse
from .models import *
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


def practice(request):
    return render(request, 'capstone/practice.html')


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