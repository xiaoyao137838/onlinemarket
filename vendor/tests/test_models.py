from django.test import TestCase
from vendor.models import Product
import pytest
from model_bakery import baker
from pprint import pprint

@pytest.mark.unit
def test_vendor_str(vendor):
    assert vendor.vendor_name == 'vendor_1'
    assert str(vendor) == 'vendor_1'

@pytest.mark.unit
def test_vendor_is_open(vendor):
    assert vendor.is_open() == False

@pytest.mark.unit
def test_product_str(product):
    assert product.name == 'product_1'
    assert str(product) == 'product_1'

@pytest.mark.unit
def test_product_clean(vendor):
    product_clean = Product(name='product_2', price=10, vendor=vendor)
    product_clean.clean()
    product_clean.save()
    product_clean = Product.objects.get(name='Product_2')
    assert product_clean.name == 'Product_2'
    assert str(product_clean) == 'Product_2'

@pytest.mark.unit
def test_opening_hour_str(opening_hour):
    assert opening_hour.day == 1
    assert str(opening_hour) == 'Monday'
 