from flashsale.forms import SaleForm, SaleOrderForm
from datetime import datetime
import tempfile
from django.test import SimpleTestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from vendor.forms import VendorForm, ProductForm, OpeningHourForm

class TestForms(SimpleTestCase):

    def test_sale_from_valid_data(self):
        form = SaleForm({
            'new_price': 10.0,
            'to_time': datetime.now(),
            'total_qty': 10,
            'available_qty': 0,
            'locked_qty': 0
        })     

        assert form.is_valid()

    def test_sale_from_invalid_data(self):
        form = SaleForm({})      
        assert form.is_valid() == False

    def test_sale_from_valid_data_init(self):
        form = SaleForm({
            'new_price': 10.0,
            'to_time': datetime.now(),
            'total_qty': 10,
            'available_qty': 0,
            'old_price': 20,
            'locked_qty': 0

        })        
        read_only_list = ['old_price', 'locked_qty']
        for field in form.fields:
            if field in read_only_list:
                assert form.fields[field].widget.attrs['readonly'] == 'readonly'

    def test_sale_order_from_valid_data(self):
        form = SaleOrderForm({
            'first_name': 'geng',
            'last_name': 'hong'
        })      
        assert form.is_valid()


    def test_sale_order_from_invalid_data(self):
        form = SaleOrderForm({})      
        assert form.is_valid()  == False 