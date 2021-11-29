from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse
from .models import *
app_name = 'pybo'

def index(request):
    # return HttpResponse("안녕하세요 pybo에 오신것을 환영합니다.")
    '''
    team 목록 출력
    '''
    team_list = Team.objects.order_by('teamName')
    context = {'team_list': team_list}
    return render(request, 'pybo/team_list.html', context) # context 의 내용을 포함해서 html 로 가는 것임. 선택 arg 이므로 안써도 됨.


def teamDetail(request, team_id):
    # team id 사용해서 team member... 빼오기
    # print(team_teamName)
    # team = get_object_or_404(TeamMember, pk=team_teamName)
    team = Team.objects.get(id=team_id)
    context = {'team': team}
    return render(request, 'pybo/team_detail.html', context)


def teamCreate(request, team_id):
    return HttpResponse("안녕하세요 pybo에 오신것을 환영합니다.")




