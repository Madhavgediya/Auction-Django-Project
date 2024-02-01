from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import  logout as auth_logout
from .forms import RegistrationForm

from .models import *

def home(request):
    product_data = Product.objects.all()
    # product_data = product_data[:3]
    # product_data = Product.objects[:3]
    product_data = Product.objects.order_by('-id')[:3]
    data = {
            'product_data':product_data,
        }
    return render(request, "home/index.html", data) 

def contact(request):
    context = {'page': 'Contact'}
    return render(request, "home/contact.html", context) 

def category(request):
    context = {'page': 'category'}
    return render(request, "home/category.html", context) 

def about(request):
    about = {'page': 'About'}
    return render(request, "home/about.html", about) 

def auction(request):
    auction = {'page': 'Auction'}
    product_data = Product.objects.all()
    data = {
            'product_data':product_data
        }
    return render(request, "home/auction.html", data) 

def user(request):
    user = {'page': 'user'}
    return render(request, "home/user.html", user) 

def mj(request):
    mj = {'page': 'mj'}
    return render(request, "home/#loginForm", mj) 


def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Password Do not match")
            return redirect('home')

        myuser = User.objects.create_user(username, email, password)
        myuser.save()
        messages.success(request, "Success")
        return redirect('home')

def my_login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login")
            return redirect('home')
        else:
            messages.error(request, "Not Login")
            return redirect('home')

    return HttpResponse('404 page')
    
def my_logout(request):
    auth_logout(request)
    messages.success(request, "Successfully logged out.")
    return redirect('home')
