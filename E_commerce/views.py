from django.shortcuts import render, redirect
from .models import Food
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialLogin
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.helpers import complete_social_login
from allauth.socialaccount.models import SocialAccount
from django.http import HttpResponse
from .services import send_sms
from .models import FoodOrdera
from .forms import FoodOrderaForm
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client


@csrf_exempt
def incoming_sms(request):
    """Handles SMS replies from customers"""
    body = request.POST.get("Body", "").strip()
    sender = request.POST.get("From", "")

    response = MessagingResponse()
    response.message(f"Thank you for your message: {body}")

    return HttpResponse(str(response), content_type="application/xml")
@login_required(login_url='about')
def place_food_order(request):
    if request.method == "POST":
        form = FoodOrderaForm(request.POST)
        if form.is_valid():
            # Save order
            food_order = form.save(commit=False)
            food_order.customer =request.user
            food_order.status = "pending"
            food_order.save()

            # Send SMS to Customer
            send_sms(food_order.phone_number, f"Hello {request.user.username}, your order has been placed and is now pending. We will notify you once it's confirmed!")

            # Send SMS to Admin
            send_sms(settings.ADMIN_PHONE_NUMBER, f"New order placed by {request.user.first_name}. Order ID: {food_order.id}, Status: Pending")

            messages.success(request, "Your food order has been placed!")
            return redirect("book")  # Redirect to a success page

    else:
        form = FoodOrderaForm()

    return render(request, "book.html", {"form": form})

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
    Foods= Food.objects.all()
    return render(request, 'index.html', {
        'Special_day': 'Christmas',
        'spcial_day': 'Eid al-Fitr',
        'Foods': Foods,
    })

def about(request):
    return render(request, 'about.html')

@login_required(login_url='about')
def book(request):
    return render(request, 'book.html')


@login_required(login_url='about')
def menu(request):
    Foods= Food.objects.all()
    return render(request, 'menu.html', {'Foods': Foods})
   

def post(request, pk):
    return render(request,'post.html', {'pk':pk} )

