from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'address', 'city', 'state', 'country', 'zip_code', 'phone', 'email',
                  'first_name_bill', 'last_name_bill', 'address_bill', 'city_bill', 'state_bill', 'country_bill', 'zip_code_bill', 'phone_bill', 'email_bill']