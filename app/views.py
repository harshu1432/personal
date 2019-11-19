from django.shortcuts import render
from django.http import HttpResponse
from app import forms

from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail


# Create your views here.
def home(request):
    return render(request,"home.html")

def register(request):
    register=False
    if request.method=='POST':
        user_form=forms.User_Form(request.POST)
        user_data_form=forms.User_data_Form(request.POST,request.FILES)
        if user_form.is_valid() and user_data_form.is_valid():
            user=user_form.save(commit=True)
            user.set_password(user.password)
            user.save()

            user_data=user_data_form.save(commit=False)
            user_data.user=user

            if 'profile_pic' in request.FILES:
                user_data.profile_pic=request.FILES['profile_pic']
                user_data.save()
                register=True
    else:
        user_form=forms.User_Form()
        user_data_form=forms.User_data_Form()

    d={'form':user_form,'form_user':user_data_form,'register':register}
    return render(request,'register.html',context=d)

def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username','')
        password=request.POST.get('password','')
        user=authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                request.session['username']=username
                return HttpResponseRedirect(reverse('afterlogin'))
            else:
                HttpResponse('Not an Active User')
        else:
            return HttpResponse('invalid login detailes')
    else:
        return render(request,'login.html')

def after_login(request):
    user_name=request.session.get('username','no user')
    Account_number=request.POST.get('Account_number','No account no')
    email=request.session.get('email','No Email')
    branch=request.session.get('Branch','No branch')
    d={'user_name':user_name,'Account_number':Account_number,'email':email,'branch':branch}
    return render(request,'afterlogin.html',context=d)

@login_required
def user_logout(request):
    logout(request)
    try:
        del request.session['username']
    except:
        pass
    return HttpResponseRedirect(reverse('login'))
