import phonenumbers
from django import forms
from .models import FoodOrdera

class FoodOrderaForm(forms.ModelForm):
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
        fields = ['customer_name', 'phone_number', 'food_item', 'quantity', 'delivery_address', 'status','total_price', 'photo']
