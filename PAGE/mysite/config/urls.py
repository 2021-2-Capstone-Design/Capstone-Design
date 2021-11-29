"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
#from pybo import views

urlpatterns = [
    path('anmu/', include('capstone.urls')), #capstone project



    path('admin/', admin.site.urls),
    path('pybo/', include('pybo.urls')), # project의 성격이므로
    path('common/', include('common.urls')),
    #http://localhost:8000/ 을 입력했을 때 바로 pybo.urls 로 가게 함
]
