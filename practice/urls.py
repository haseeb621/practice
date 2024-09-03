from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from Account.views import password_reset,password_reset_complete,password_reset_confirm,password_reset_done


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Bank.urls', namespace='Bank')),
    path('Account/', include('Account.urls', namespace='Account')),  # Added a trailing slash
    
   
]
admin.site.site_header="BANK MANAGMENT"
admin.site.site_title="Bank info"
admin.site.site_url="BANK"
admin.site.index_title="editor"
