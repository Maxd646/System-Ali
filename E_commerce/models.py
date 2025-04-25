from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from .services import send_sms
from django.conf import settings

class FoodOrdera(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    customer_name = models.CharField(max_length=100)
    food_item = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    delivery_address = models.TextField()
    your_photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)  # Ensure it's in E.164 format (+251...)
    transaction = models.ImageField(upload_to='photos/', null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """ Send SMS to Customer & Admin when the order status changes """
        if self.pk:  # If order exists (not first creation)
            original = FoodOrdera.objects.get(pk=self.pk)
            if original.status != self.status:
                
                message = f"Your order #{self.id} is now {self.status} by Alamnew foor delivery"
                send_sms(self.phone_number, message)
                    
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.id} - {self.customer.username} ({self.status})"

class Customer(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    food_preference = models.CharField(max_length=100)
    customer_id = models.CharField(max_length=50, unique=True)
    photo = models.ImageField(upload_to='customer_photos/')

    def __str__(self):
        return self.full_name
    
    
class Food(models.Model):
    name = models.CharField(max_length=255, unique=True)  
    description = models.TextField()  
    price = models.DecimalField(max_digits=10, decimal_places=2)  
    category = models.CharField(max_length=20)
    available = models.BooleanField(default=True)  
    image = models.ImageField(upload_to='food_images/', null=True, blank=True) 
    
    def __str__(self):
        return self.name

class ItemFeedback(models.Model):
    name = models.CharField(max_length=100)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class FoodItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='food_images/')  # Use MEDIA_URL & MEDIA_ROOT

    def __str__(self):
        return self.title
    
class DeviceItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    image = models.ImageField(upload_to='device_images/')  # Use MEDIA_URL & MEDIA_ROOT

    def __str__(self):
        return self.title
     