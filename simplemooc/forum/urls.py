from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('tag/<tag>/', views.index, name='index_tagged'),
    path('replies/<pk>/correct/', views.reply_correct, name='reply_correct'),
    path('respostas/<pk>/incorrect/', views.reply_incorrect, name='reply_incorrect'),
    path('<slug:slug>/', views.thread, name='thread'),
]