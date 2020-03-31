from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.courses, name='index'),
    path('<slug:slug>', views.detail, name='detail'),
]