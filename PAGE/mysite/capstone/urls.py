from django.urls import path

from . import start_practice
from . import views
from . import test1
from . import test2
from . import finaltest
from . import step



from django.contrib.auth import views as auth_views
from django.conf.urls import url

app_name = 'capstone'

urlpatterns = [
    url(r'^external', views.practice , name = 'external'),



    path('', views.main, name='main'),
    path('firstpage/', views.first, name='first'),
    path('team/', views.team, name='team'),
    path('songlist/', views.songlist, name='songlist'),

    path('practice/', views.practice, name='practice'),
    # path('practice/', finaltest.testmain, name='practice'),
    #path('practice/', views.practice, name='practice'),
    path('practice/<str:songname>/', views.practice_detail, name='songpractice'),
    path('practice/<str:songname>/step1/', step.step1main ),
    path('practice/<str:songname>/step2/', step.step2main ),
    path('practice/<str:songname>/step3/', step.step3main ),

    # path('practice/<str:songname>/step1', finaltest.testmain, name='practice'),
    # path('practice/<str:songname>/step2', finaltest.testmain, name='practice'),
    # path('practice/<str:songname>/', finaltest.testmain, name='practice'),
    


    path('record/', views.record, name='record'),
    #path('mypage/', views.mypage, name='mypage'),
    # path('mypage/', finaltest.testmain, name='mypage'),
    #path('mypage/', test2.testmain, name='mypage'),
    #path('mypage/', test1.testmain, name='mypage'),
    #path('waiting/', views.waiting, name='waiting'),
   

    path('login/',auth_views.LoginView.as_view(template_name='capstone/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('team/', views.team, name='team'),
    # path('firstpage/', views.first, name='first'),
    # path('<int:team_id>/', views.teamDetail, name='detail'),
    # path('team/create/<int:team_id>/', views.teamCreate, name='team_create')

    # path('camera/',camera.
]