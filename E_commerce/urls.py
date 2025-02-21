from django.urls import path
from .import views
from .views import place_food_order
from . import consumers

urlpatterns = [
    
    path('', views.about, name='about'),
    path('index/', views.index, name='index'),
    path('book/', views.book, name='book'),
    path('menu/', views.menu, name='menu'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name="logout"),
    path('google/', views.google_login, name="google_login"),
    path('post/<str:pk>',views.post, name="post"),
    path("order", views.place_food_order, name="book"), 
    path("sms-response", views.incoming_sms, name="incoming_sms"),
]

websocket_urlpatterns = [
    path('ws/order/<int:order_id>/', consumers.OrderConsumer.as_asgi()),
]