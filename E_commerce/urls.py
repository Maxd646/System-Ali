from django.urls import path
from .import views

urlpatterns = [
    path('', views.about, name='about'),
    path('create/', views.customer_create, name='customer_create'),
    path('index/', views.index, name='index'),
    path('book/', views.book, name='book'),
    path('menu/', views.menu, name='menu'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name="logout"),
    path('google/', views.google_login, name="google_login")
]
