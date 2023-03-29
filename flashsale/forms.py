from django import forms
from .models import FlashSale, FlashOrder

class SaleForm(forms.ModelForm):
    class Meta:
        model = FlashSale
        fields = ['old_price', 'new_price', 'from_time', 'to_time', 'total_qty', 'locked_qty', 'available_qty', 'is_active']

    def __init__(self, *args, **kwargs):
        super(SaleForm, self).__init__(*args, **kwargs)
        read_only_list = ['old_price', 'total_qty', 'locked_qty', 'available_qty']
        for field in self.fields:
            if field in read_only_list:
                self.fields[field].widget.attrs['readonly'] = 'readonly'

class SaleOrderForm(forms.ModelForm):
    class Meta:
        model = FlashOrder
        fields = ['first_name', 'last_name', 'address', 'city', 'state', 'country', 'zip_code', 'phone', 'email']