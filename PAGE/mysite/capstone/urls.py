from django.urls import path
from . import views
from . import test1
from django.contrib.auth import views as auth_views

app_name = 'capstone'

urlpatterns = [
    path('', views.main, name='main'),
    path('firstpage/', views.first, name='first'),
    path('team/', views.team, name='team'),
    path('songlist/', views.songlist, name='songlist'),
    path('practice/', views.practice, name='practice'),
    path('record/', views.record, name='record'),


    path('mypage/', test1.testmain, name='mypage'),
    #path('mypage/', views.mypage, name='mypage'),

    path('login/',auth_views.LoginView.as_view(template_name='capstone/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('team/', views.team, name='team'),
    # path('firstpage/', views.first, name='first'),
    # path('<int:team_id>/', views.teamDetail, name='detail'),
    # path('team/create/<int:team_id>/', views.teamCreate, name='team_create')

    # path('camera/',camera.
]