from django.shortcuts import render, redirect
from .forms import CustomerForm
from .models import Customer,Food
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialLogin
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.helpers import complete_social_login
from allauth.socialaccount.models import SocialAccount

def user_login(request):
    if request.method == "POST":  
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password) 
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in.')
            return redirect("index")  
        else:
            messages.error(request, 'Invalid credentials')
            return redirect("about")  
    else:
    
        return redirect("about")

def google_login(request):
    google_adapter = GoogleOAuth2Adapter()
    app = google_adapter.get_provider().get_app(request)
    sociallogin = SocialLogin(request, app, google_adapter)
    
   
    try:
        user = sociallogin.account.user
        login(request, user)
        messages.success(request, 'Successfully logged in with Google')
        return redirect('index')
    except SocialLogin.DoesNotExist:
        messages.error(request, 'Google login failed')
        return redirect('about')

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
                return redirect('about')
            elif User.objects.filter(email=email).exists(): 
                messages.info(request, 'Email already taken')
                return redirect('about')
            else:
                user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
                user.save()  
                messages.success(request, 'User Register successfully and please login')
                return redirect("about") 
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('about')
    else:
        return redirect('about')  
    
def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("about")


@login_required(login_url='about')
def index(request):
    
    return render(request, 'index.html', {
        'Special_day': 'Christmas',
        'spcial_day': 'Eid al-Fitr',
    })

def about(request):
    return render(request, 'about.html')

@login_required(login_url='about')
def book(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES)  
        if form.is_valid():
            form.save()  
            return redirect('menu')  
    else:
        form = CustomerForm() 
    
    return render(request, 'book.html', { 'form':form })

@login_required(login_url='about')
def menu(request):
    Foods= Food.objects.all()
    return render(request, 'menu.html', {'Foods': Foods})

def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('menu')  
    else:
        form = CustomerForm()
    return render(request, 'E_commerce/customer_form.html', {'form': form})
