from django.contrib import admin
from django.urls import path ,include
from .views import *

app_name='Account'

urlpatterns = [
    path('register/', register, name='register'),
    path('render_register/', render_register, name='render_register'),
    path('Login/', Login, name="Login"),
    path('render_Login/', render_Login, name="render_Login"),
    path('Logout/', Logout, name="Logout"),
    path('profile/', profile, name="profile"),
    path('success_login/', success_login, name='success_login'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('render_edit_profile/', render_edit_profile, name='render_edit_profile'),
    path('profile2/', profile2, name='profile2'),
    path('change_pass/', change_pass, name='change_pass'),
    path('render_change_pass/', render_change_pass, name='render_change_pass'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('login_activate/<uidb64>/<token>/', login_activate, name='login_activate'),
    
    path('password_reset/', password_reset, name='password_reset'),
    path('password_reset/done/', password_reset_done, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', password_reset_complete, name='password_reset_complete'),
]