from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.courses, name='index'),
    path('<slug:slug>', views.detail, name='detail'),
    path('<slug:slug>/enroll/', views.enrollment, name='enrollment'),
    path('<slug:slug>/enroll/cancel', views.undo_enrollment, name='undo_enrollment'),
    path('<slug:slug>/announcements/', views.announcements, name='announcements'),
    path('<slug:slug>/announcements/<pk>/', views.show_announcement, name='show_announcement'),
    path('<slug:slug>/lessons/', views.lessons, name='lessons'),
    path('<slug:slug>/lesson/<pk>/', views.lesson, name='lesson'),
    path('<slug:slug>/materials/<pk>/', views.material, name='material'),
]