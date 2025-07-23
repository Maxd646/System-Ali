from django.shortcuts import render, redirect
from .models import Food, FoodItem, DeviceItem, FoodOrdera, Customer, ItemFeedback
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialLogin, SocialAccount
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.helpers import complete_social_login
from .services import send_sms
from .forms import FoodOrderaForm
from django.conf import settings
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import FoodItemSerializer, DeviceItemSerializer, FoodOrderaSerializer, CustomerSerializer, FoodSerializer, ItemFeedbackSerializer
from rest_framework import generics
from rest_framework.views import APIView


def search_items(request):
    query = request.GET.get('query', '')

    food_results = Food.objects.filter(name__icontains=query).values('name', 'description', 'price', 'image', 'category', 'available')
    food_results = FoodItem.objects.filter(name__icontains=query).values('title', 'description','price', 'image')
    device_results = DeviceItem.objects.filter(name__icontains=query).values('title', 'description','price', 'image')
    
    return JsonResponse({
        'food_items': list(food_results),
        'devices': list(device_results),
    })

class FoodItemList(APIView):
    def get(self, request):
        items = FoodItem.objects.all()
        serializer = FoodItemSerializer(items, many=True)
        return Response(serializer.data)
class DeviceItemList(APIView):
    def get(self, request):
        items = DeviceItem.objects.all()
        serializer = DeviceItemSerializer(items, many=True)
        return Response(serializer.data)

class FoodOrderaListCreateView(generics.ListCreateAPIView):
    queryset = FoodOrdera.objects.all()
    serializer_class = FoodOrderaSerializer

class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class FoodListCreateView(generics.ListCreateAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer

class ItemFeedbackListCreateView(generics.ListCreateAPIView):
    queryset = ItemFeedback.objects.all()
    serializer_class = ItemFeedbackSerializer


def item_feedback(request, item_id):
    item = get_object_or_404(ItemFeedback, pk=item_id)

    if request.method == 'POST':
        if 'like' in request.POST:
            item.likes += 1
        elif 'dislike' in request.POST:
            item.dislikes += 1

        item.save() 

    return render(request, 'feedback/item_feedback.html', {'item': item})


def menu_view(request):
    category = request.GET.get('category', 'all')

    if category == 'all':
        foods = Food.objects.all()
    else:
        foods = Food.objects.filter(category=category)

    # get distinct categories from the database
    categories = Food.objects.values_list('category', flat=True).distinct()

    return render(request, 'menu.html', {
        'foods': foods,
        'selected_category': category,
        'categories': categories,
    })

def login_required_message(view_func):
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in before accessing this page.")
            return redirect('about')  # Redirect to about page
        return view_func(request, *args, **kwargs)
    return wrapped_view

@csrf_exempt
def incoming_sms(request):
    """Handles SMS replies from customers"""
    body = request.POST.get("Body", "").strip()
    sender = request.POST.get("From", "")

    response = MessagingResponse()
    response.message(f"Thank you for your message: {body}")

    return HttpResponse(str(response), content_type="application/xml")

@login_required_message
def place_food_order(request):
    if request.method == "POST":
        form = FoodOrderaForm(request.POST)
        if form.is_valid():
            food_order = form.save(commit=False)
            food_order.customer = request.user
            food_order.status = "pending"
            food_order.save()

            send_sms(food_order.phone_number, f"Hello {request.user.username}, your order has been placed and is now pending. We will notify you once it's confirmed!")
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
                messages.success(request, 'User registered successfully. Please log in.')
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

@login_required_message
def index(request):
    Foods = Food.objects.all()
    return render(request, 'index.html', {
        'Special_day': 'Christmas',
        'spcial_day': 'Eid al-Fitr',
        'Foods': Foods,
    })

def about(request):
    return render(request, 'about.html')

@login_required_message
def book(request):
    return render(request, 'book.html')

@login_required_message
def menu(request):
    Foods = Food.objects.all()
    return render(request, 'menu.html', {'Foods': Foods})

def post(request, pk):
    return render(request, 'post.html', {'pk': pk})
