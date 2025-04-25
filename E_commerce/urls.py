from django.urls import path
from .import views 
from django.urls import path, include
from .views import *
from .admin import *
from . import consumers
from django.urls import path
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter

urlpatterns = [
    path('E_commerce/food/', FoodItemList.as_view(), name='food-list'),
    path('E_commerce/device/', DeviceItemList.as_view(), name='device-list'),
    path('', views.about, name='about'),
    path('index/', views.index, name='index'),
    path('book/', views.book, name='book'),
    path('menu/', views.menu, name='menu'),
    path('auth/', include('dj_rest_auth.urls')),  # login/logout
    path('auth/registration/', include('dj_rest_auth.registration.urls')),  # register
    path('auth/', include('allauth.socialaccount.urls')),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name="logout"),
    path('google/', views.google_login, name="google_login"),
    path('post/<str:pk>',views.post, name="post"),
    path("order", views.place_food_order, name="book"), 
    path("sms-response", views.incoming_sms, name="incoming_sms"),
    path('menu/', views.menu_view, name='menu'),
    path('feedback/<int:item_id>/', views.item_feedback, name='item_feedback'),
]

websocket_urlpatterns = [
    path('ws/order/<int:order_id>/', consumers.OrderConsumer.as_asgi()),
]