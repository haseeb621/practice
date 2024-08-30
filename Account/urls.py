from django.contrib import admin
from django.urls import path ,include
from .views import *
app_name='Account'

urlpatterns = [
 path('register',register,name='register'),
 path('Login',Login,name="Login"),
 path('Logout',Logout,name="Logout"),
 path('profile',profile,name="profile"),
 path('success_login',success_login,name='success_login'),
 path('edit_profile',edit_profile,name='edit_profile'),
 path('profile2',profile2,name='profile2'),
 path('reset_pass',reset_pass,name='reset_pass'),
 path('activate/<uidb64>/<token>',activate,name='activate'),
 path('login_activate/<uidb64>/<token>',login_activate,name='login_activate')
]