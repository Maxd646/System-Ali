from django.contrib import admin
from .models import *
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


admin.site.site_title = "Daniboy Admin Portal"
admin.site.site_header = 'Alamnew Online Food Delivery'
admin.site.index_title = "Welcome to the Alamnew Admin Panel"


admin.site.register(ItemFeedback)
def update_order_status(order_id, new_status):
    order = FoodOrdera.objects.get(id=order_id)
    order.status = new_status
    order.save()

    # Send real-time update to WebSocket
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"order_{order.id}",
        {
            "type": "order_status_update",
            "status": order.status,
        }
    )


@admin.register(FoodOrdera)
class FoodOrderaAdmin(admin.ModelAdmin):
    list_display=('customer_name', 'food_item', 'phone_number','created_at')
    search_fields =('food_item',)
    list_filter =( 'food_item', )
    fieldsets = (
        (None, {'fields': (('customer_name', 'food_item', 'quantity', ), 'phone_number', )}),
        ('Extra into', {
                        'classes': ('collapse',),
                       'fields':('status', 'photo', 'delivery_address') 
                       }), 
        )

@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display=('title', 'description', 'price', 'image')

@admin.register(DeviceItem)
class DeviceItemAdmin(admin.ModelAdmin):
    list_display=('title', 'description', 'price', 'image')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'food_preference', 'customer_id', 'photo')
    search_fields = ('full_name', 'email') 
    list_filter= ('full_name', 'phone_number')
   
@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):

    list_display= ('name', 'available', 'price', 'category')
    list_display_links=('name',)
    list_filter =( 'available',)
    search_fields=('name', 'price')
    list_per_page=3
    fieldsets = (
        (None, {'fields': (('name', 'available'), 'price', 'category')}),
        ('Extra into', {
                        'classes': ('collapse',),
                       'fields':('description', 'image') 
                       }), 
        )
    
    list_editable= ('price', 'available')

