from django.urls import path
from . import views
app_name = 'pybo'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:team_id>/', views.teamDetail, name='detail'),
    path('team/create/<int:team_id>/', views.teamCreate, name='team_create')

    # path('camera/',camera.
]
