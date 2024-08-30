from django.urls import path
from . import views

app_name = 'Bank'

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('Accounts', views.Accounts, name='Accounts'),
    path('add', views.add, name='add'),
    path('delete/<int:id>', views.delete_bank, name='delete_bank'),
    path('add_branch/<int:id>',views.add_branch,name='add_branch'),
    path('branch_view/<int:id>',views.branch_view,name='branch_view'),
    path('branch_edit/<int:id>',views.branch_edit,name='branch_edit'),
]

