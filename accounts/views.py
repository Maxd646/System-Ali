from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


def user_login(request):
    if request.method == "POST":  
        username = request.POST["username"]
        password = request.POST["password"]
        user =authenticate(request, username=username, password=password) 
        
        if user is not None:
           login(request, user) 
           messages.success(request, 'Successfuly login') 
           return redirect("index")  
        else:
            messages.error(request, 'Invalid credentials')
            return redirect("index")  
    else:
        return redirect('index')  


def register(request):
    if request.method == 'POST':  
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():  
                messages.info(request, 'Username already taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists(): 
                messages.info(request, 'Email already taken')
                return redirect('index')
            else:
                user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                user.save()  
                messages.success(request, 'User created successfully')
                return redirect("index") 
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('index')
    else:
        return redirect('index')  
    
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("index")

