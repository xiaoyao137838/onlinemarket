from django.test import TestCase
from vendor.models import Product, OpeningHour
import pytest
from model_bakery import baker
from pprint import pprint

class TestProduct(TestCase):

    def setUp(self):
        self.prod_2 = Product(name='test_2')

    def test_str(self):
        self.assertEqual(str(self.prod_2), 'test_2')

class TestOpeningHour(TestCase):

    def setUp(self):
        self.opening_hour_1 = OpeningHour(day=7)
        self.opening_hour_2 = OpeningHour(day=8)

    # def test_str(self, vendor_test):
    #     self.assertEqual(str(self.opening_hour_1), 'Sunday')
    #     assert str(vendor_test) == 'vendor_test'

@pytest.mark.unit
def test_vendor_creation(vendor_test, session):
    assert str(vendor_test) == 'vendor_test'