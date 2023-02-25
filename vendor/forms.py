from django import forms
from .models import Vendor, Product, OpeningHour
from accounts.validators import validate_picture_format

class VendorForm(forms.ModelForm):
    verified_file = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}),validators= [validate_picture_format])

    class Meta:
        model = Vendor
        fields = ['vendor_name', 'verified_file']

class ProductForm(forms.ModelForm):
    image = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}),validators= [validate_picture_format])

    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'image', 'is_available']

class OpeningHourForm(forms.ModelForm):
    class Meta:
        model = OpeningHour
        fields = ['day', 'from_time', 'to_time', 'is_closed']
        