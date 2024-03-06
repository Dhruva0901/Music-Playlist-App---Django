# Create your views here.
# imported our models
from django.core.paginator import Paginator
from django.shortcuts import render, HttpResponse, redirect
from cgitb import text
from contextvars import Context
import email
import string
import uuid
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User, auth
from django.contrib import messages
from . models import Song
from django.views.generic import ListView, DetailView


def signup(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password==confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username is already taken')
                return redirect('/signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email is already taken')
                return redirect('/signup')
            else:
                user = User.objects.create_user(username=username, password=password, 
                                        email=email, first_name=first_name, last_name=last_name)
                user.save()
                
                return redirect('/list')


        else:
            messages.info(request, 'Both passwords are not matching')
            return redirect('/signup')

            

    else:
        return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/list')
        elif User.objects.filter(email = username).exists() == False:
            messages.info(request, "Username or Password incorrect.Try Again")
            return redirect('/')
        else:
            messages.info(request, 'Invalid Username or Password')
            return redirect('/')
    else:
        return render(request, 'login.html')
    
def logout(request):
    auth.logout(request)
    return redirect('/list')

def home(request):
    paginator= Paginator(Song.objects.all(),1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={"page_obj":page_obj}
    return render(request,"home.html",context)


class musiclist(ListView):
    model = Song
    template_name = "list.html"
    context_object_name = "music"

class musicdetail(DetailView):
    model = Song
    template_name = "page.html"
    context_object_name = "music"

def forgetpass(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        re_password = request.POST['re_password']
        user = User.objects.get(email = email)
        if User.objects.filter(email = email).exists():
            if password == re_password:
                user.set_password(password)
                user.save()
                return render(request, 'login.html')
            else:
                messages.info(request,'Passwords doesnot match')
                return redirect('/forgetpass')
        else:
            messages.info(request,'User doesnot exist! Please Sign up')
            return redirect('/signup')
    else:
        return render(request, 'forgetpass.html')