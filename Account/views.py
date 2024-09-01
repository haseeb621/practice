from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy
import Bank
from django.core.validators import EmailValidator
from Bank.models import Bank
from django.http import JsonResponse
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.template.loader import render_to_string
from practice import settings
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.contrib.auth.views import PasswordResetCompleteView,PasswordResetConfirmView,PasswordResetDoneView,PasswordResetView


def render_register(request):
  return render(request,'register.html')
@require_POST
def register(request):
  fname=request.POST['fname']
  lname=request.POST['lname']
  uname=request.POST['uname']
  email=request.POST['email']
  pass1=request.POST['pass1']
  pass2=request.POST['pass2']
  

  
  email_validator=EmailValidator()
  try:
    email_validator(email)
    valid_email=True
  except:
    valid_email=False
    messages.error(request,'Enter a valid email address')
    return render(request,'login.html')
  if User.objects.filter(username=uname):
    messages.error(request,'A user with that username already exists')
    return redirect('Account:register')
  elif pass1!=pass2:
    messages.error(request,"The two password fields didn't match")
    return redirect('Account:register')
  elif len(str(pass1))<8:
    messages.error(request,'This password is too short. It must contain at least 8 characters')
    return redirect('Account:register')
  elif not valid_email:
    messages.error(request,'Enter a valid email address')
    return redirect('Account:register')

  else:
   myuser=User.objects.create_user(uname,email,pass1)
   myuser.first_name=fname
   myuser.last_name=lname
   myuser.is_active=False
   
   site=get_current_site(request)

    
   subject="This is a confirmation email to register your account on django preoject"
   message=render_to_string('confirmation_mail.html',{
     'user':User.first_name,
     'domain':site.domain,
     'uid':urlsafe_base64_encode(force_bytes(myuser.pk)),
     'token':default_token_generator.make_token(myuser),
     
   })
   to_list=[myuser.email]
   from_mail=settings.EMAIL_HOST_USER
   send_mail(subject,message,from_mail,to_list,fail_silently=True)
   messages.info(request,'A Varification email was sent successfully')
   myuser.save()
   return redirect('Account:render_Login')
def render_Login(request):
  return render(request,'login.html')
@require_POST
def Login(request):
  uname=request.POST['uname']
  pass1=request.POST['pass1']
  user=authenticate(username=uname,password=pass1)
  
  if user is not None:
   site=get_current_site(request)
   subject='2FA varification'
   message=render_to_string('login_mail.html',{
     'user':user.first_name,
     'domain':site.domain,
     'uid':urlsafe_base64_encode(force_bytes(user.pk)),
     'token':default_token_generator.make_token(user)
   })
   from_mail=settings.EMAIL_HOST_USER
   to_list=[user.email]
   send_mail(subject,message,from_mail,to_list,fail_silently=True)
   messages.info(request,'2FA verification required')
   return render(request,'login.html')
  else:
    messages.error(request,'Username or passwword incorrect')
    return redirect('Account:render_Login')
def success_login(request):
  banks = Bank.objects.filter(owner=request.user)
  return render(request, 'success_login.html', {'banks': banks})
def profile(request):
 user=request.user
 userData={ "uname": user.username,
        "email": user.email,
        "fname": user.first_name,
        "lname": user.last_name,
         "pk":user.pk,
         }
 return JsonResponse(userData)

def render_edit_profile(request):
  return render(request,'edit_profile.html')  
@require_POST
def edit_profile(request):
   email=request.POST['email']
   fname=request.POST['fname']
   lname=request.POST['lname']
   uname=request.POST['uname']
   
   user=request.user
   user.username=uname
   user.first_name=fname
   user.last_name=lname
   user.email=email
   user.save()
   
   messages.success(request,'Your profile was edited successfully')
   return redirect('Account:profile2') 
def profile2(request):
  return render(request,'profile.html')
def Logout(request):
  logout(request)
  banks=Bank.objects.all()
  return render(request,'index.html',{'banks':banks})
def render_change_pass(request):
  return render(request, 'change_pass.html')
@require_POST
def change_pass(request):
     user=request.user
     uname = request.POST['uname']
     pass1 = request.POST['pass1']
     if len(str(pass1))< 8:
       messages.error(request,'Paswword must be 8 characters')
       return redirect('Account:forget_pass')
     elif user.username!=uname:
       messages.error(request,'Invalid Username')
       return render(request,'change_pass.html')
     else:
      try:
        user = User.objects.get(username=uname)
        user.set_password(pass1)
        user.save()
        messages.success(request, 'Password successfully changed')
        return redirect('Account:render_Login')  # Redirect to a success page or profile page
      except User.DoesNotExist:
              messages.error(request, 'Wrong username.')
              return render(request, 'change_pass.html')
def activate(request,uidb64,token):
  try:
    uid=urlsafe_base64_decode(force_str(uidb64))
    user=User.objects.get(pk=uid)
  except(TypeError,ValueError,User.DoesNotExist):
    user=None
    
  if user is not None and default_token_generator.check_token(user,token):
    user.is_active=True
    user.save()
    return redirect('Account:render_Login')
def login_activate(request,uidb64,token):
 try:
  uid=urlsafe_base64_decode(force_str(uidb64))
  user=User.objects.get(pk=uid)
 except(TypeError,ValueError,User.DoesNotExist):
  user=None
     
 if user is not None and default_token_generator.check_token(user,token):
  login(request,user)
  return redirect('Account:success_login')
 else:
  return render(request,'activation_failed.html') 
def password_reset(request):
    return PasswordResetView.as_view(
        template_name='reset/password_reset_form.html',
        email_template_name='reset/password_reset_email.html', 
        success_url=reverse_lazy('Account:password_reset_done')
    )(request)
def password_reset_done(request):
    return PasswordResetDoneView.as_view(
        template_name='reset/password_reset_done.html'
    )(request)
def password_reset_confirm(request, uidb64, token):
    return PasswordResetConfirmView.as_view(
        template_name='reset/password_reset_confirm.html',
        success_url=reverse_lazy('Account:password_reset_complete')
    )(request, uidb64=uidb64, token=token)
def password_reset_complete(request):
    return PasswordResetCompleteView.as_view(
        template_name='reset/password_reset_complete.html'
)(request)
