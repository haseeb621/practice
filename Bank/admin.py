from django.contrib import admin
from .models import Bank,Branch

class MyBank(admin.ModelAdmin):
  list_display=['name','description','inst_num','swift_code','owner']
  search_fields=['name','inst_num']
admin.site.register(Bank,MyBank)

class MyBranch(admin.ModelAdmin):
   list_display=['name','transit_num','email','Bank_id']
   search_fields=['name']
admin.site.register(Branch,MyBranch)

