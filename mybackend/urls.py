# mybackend/urls.py
from django.contrib import admin
from django.urls import path, include
 

urlpatterns = [
    path('', include('E_commerce.urls')),  # This handles index, about, and book
    path('admin/', admin.site.urls),
]
