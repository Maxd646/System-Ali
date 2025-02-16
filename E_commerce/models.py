from django.db import models

# Create your models here.
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
    category = models.CharField(max_length=100) 
    available = models.BooleanField(default=True)  
    image = models.ImageField(upload_to='food_images/', null=True, blank=True) 

    def __str__(self):
        return self.name  


        