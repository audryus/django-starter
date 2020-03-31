from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_view

from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('signup/', views.register, name='signup'),
    path('edit/', views.edit, name='edit'),
    path('edit/password/', views.edit_password, name='edit_password'),
    path('signin/', auth_view.LoginView.as_view(template_name='accounts/signin.html'), name='signin'),
    path('logout/', auth_view.LogoutView.as_view(next_page='core:home'), name='logout'),
]