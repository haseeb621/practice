from django.contrib import messages
from django.shortcuts import get_object_or_404, render,redirect

import Account
from .models import Bank,Branch
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
 banks=Bank.objects.all()
 return render(request,'index.html',{'banks':banks})
def about(request):
 return render(request,'about.html')
def Accounts(request):
 return render(request,'Accounts.html')
@login_required
def add(request):
 if request.method=='POST':
  name=request.POST['name']
  desc=request.POST['desc']
  inst_num=request.POST['inst_num']
  swift_code=request.POST['swift_code']
  
  bank =Bank(name=name,
            description=desc,
            inst_num=inst_num,
            swift_code=swift_code,
            owner=request.user)
  bank.save()
  
  return redirect('Account:success_login')
 return render(request,'add.html')
@login_required
def delete_bank(request,id):
 bank=get_object_or_404(Bank ,id=id)
 if bank.owner==request.user:
  bank.delete()
 return redirect('Account:success_login')
@login_required
def add_branch(request,id):
 if request.method=='POST':
  name=request.POST['name']
  transit_num=request.POST['transit_num']
  email=request.POST['email']
  capacity=request.POST['capacity']

  bank=get_object_or_404(Bank ,id=id)  
  branch=Branch.objects.create(
   name=name,
   transit_num=transit_num,
   email=email,
   capacity=capacity,
   Bank_id=bank,
  )
  messages.success(request,'Branch added successfully')
  return render(request,'add_branch.html',{'id':id})
 return render(request,'add_branch.html',{'id':id})
def branch_view(request,id):
 bank=get_object_or_404(Bank,id=id)
 branch=bank.branches.all()
 return render(request,'branch_view.html',{'branches':branch,'bank':bank})
@login_required
def branch_edit(request, id):
    branch = get_object_or_404(Branch, id=id)
    
    if request.method == 'POST':
        branch.name = request.POST['name']
        branch.transit_num = request.POST['transit_num']
        branch.email = request.POST['email']
        branch.capacity = request.POST['capacity']
        branch.save()
        messages.success(request, 'Branch updated successfully')
        return render(request,'branch_edit.html',{'id':id})
    
    return render(request, 'branch_edit.html', {'branch': branch,'id':id})
def prac(request):
    return render(request,"prac.html")