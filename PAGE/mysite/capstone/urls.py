from django.urls import path

from . import views
from . import step



from django.contrib.auth import views as auth_views
from django.conf.urls import url

app_name = 'capstone'

urlpatterns = [

    path('', views.main, name='main'),
    path('demo_intro/', views.demo_intro, name='intro'),
    path('demo_practice/', views.demo_practice, name='practice'),
    path('demo_upload/', views.demo_upload, name='upload'),
    path('demo_history/', views.demo_history, name='history'),
    path('demo_extract', views.demo_extract, name='extract'),
    path('demo_film/', views.demo_film, name='film'),
    path('demo_score/', views.demo_score, name='score'),
    # path('practice/', finaltest.testmain, name='practice'),
    #path('practice/', views.practice, name='practice'),




    #path('demo_practice/<str:songname>/', step.practice_detail, name='songpractice'),
    
    # 원래 있는 파일
    path('demo_practice/<str:songname>/step1/', step.step1main,name = 'step1' ),
    path('demo_practice/<str:songname>/step2/', step.step2main,name = 'step2' ),
    # path('demo_practice/<str:songname>/step3/', step.step3main,name = 'step3' ),

    # 업로드 할 때
    path('demo_practice/C:/fakepath/<str:songpath>/choosenum/', step.choosenum ), # 파일 업로드 하고 누르면 해당 파일 정보를 가지고 몇명을 선택할 지 선택하는 창
    
    # 업로드 후 1인이라고 할 때
    path('demo_practice/<str:songname>/userinput/step1/', step.userstep1main, name = 'userstep1' ),
    #path('practice/C:/fakepath/<str:songpath>/choosenum/', step.choosenum ),
    # path('practice/userinput/chooseperson/', step.chooseperson ),
    # path('practice/userinput/1/getsong/', step.practice ),

    # 업로드 후 2인이라고 할 때 crop
    path('demo_practice/<str:songname>/crop/', step.cropping, name = 'crop_and_extract' ),
    path('demo_practice/<str:songname>/demo_score/', step.step2main, name = 'demo_score'),
    path('demo_practice/<str:songname>/<int:num>/', step.extract, name = 'extract' ),



    #path('demo_practice/<str:songname>/<int:peoplenum>/', step.practice_detail, name = 'step0'),



]