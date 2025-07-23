import phonenumbers
from django import forms
from .models import *

class FoodOrderaForm(forms.ModelForm):
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Enter phone number', 'class': 'form-control'}),
        label="Phone Number"
    )
    delivery_address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'class': 'form-control', 'placeholder': 'Enter delivery address'}),
        label="Delivery Address"
    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        try:
            parsed_number = phonenumbers.parse(phone_number, None)
            if not phonenumbers.is_valid_number(parsed_number):
                raise forms.ValidationError("Invalid phone number format.")
        except phonenumbers.NumberParseException:
            raise forms.ValidationError("Invalid phone number format.")

        return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)

    class Meta:
        model = FoodOrdera
        fields = ['customer_name', 'phone_number', 'food_item', 'quantity', 'delivery_address', 'status', 'transaction', 'your_photo']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full name'}),
            'food_item': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Food item'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'transaction': forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'Enter screenshot of transaction'}),
            'your_photo': forms.ClearableFileInput(attrs={'class': 'form-control', 'placeholder': 'Enter your photo'}),
        }