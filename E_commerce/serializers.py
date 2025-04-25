from rest_framework import serializers
from .models import *

class FoodOrderaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodOrdera
        fields = '__all__'

class FoodOrderaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodOrdera
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'

class ItemFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemFeedback
        fields = '__all__'

class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = '__all__'
class DeviceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceItem
        fields = '__all__'
