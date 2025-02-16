from django.contrib import admin
from .models import Food
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'food_preference', 'customer_id', 'photo')
    search_fields = ('full_name', 'email')  
admin.site.register(Food)

