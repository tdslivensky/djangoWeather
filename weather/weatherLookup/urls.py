from django.urls import path

#from this directory import the views module
from . import views

urlpatterns = [
    path('', views.Home, name = "Home"),
    path('about', views.about, name = "about"),
]