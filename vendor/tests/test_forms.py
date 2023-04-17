import tempfile
from django.test import SimpleTestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from vendor.forms import VendorForm, ProductForm, OpeningHourForm

class TestForms(SimpleTestCase):

    def test_vendor_form_valid_data(self):
        form = VendorForm(data={
            'vendor_name': 'form_1',
            
        },
        files={
            'verified_file': SimpleUploadedFile("file.jpg", b"file_content")
        })
    
        self.assertTrue(form.is_valid())

    def test_vendor_form_no_dada(self):
        form = VendorForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)

    def test_product_form_valid_data(self):
        form = ProductForm(data={
            'name': 'product_2', 
            'price': 0.92, 
            'description': 'Good product',
        },
        files={
            'image': SimpleUploadedFile("file.jpg", b"file_content")
        })

        self.assertTrue(form.is_valid())

    def test_product_form_no_dada(self):
        form = ProductForm(data={})
        for error in form.errors:
            print(error)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

    def test_opening_hour_form_valid_data(self):
        form = OpeningHourForm(data={
            'day': 1
        })

        self.assertTrue(form.is_valid())

    def test_opening_hour_form_no_dada(self):
        form = OpeningHourForm(data={})
        for error in form.errors:
            print(error)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)