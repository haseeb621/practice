
from django.contrib import admin
from django.urls import path ,include
from django.contrib.auth import views as auth_views
from Account.views import password_reset_complete

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('Bank.urls',namespace='Bank')),
    path('Account',include('Account.urls',namespace='Account')),
    
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/',password_reset_complete, name='password_reset_complete'),
]
