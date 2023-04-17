from django.test import RequestFactory
from django.core.exceptions import PermissionDenied
from flashsale.utils import generate_order_no, check_role_vendor, check_role_customer, get_role_url
import pytest 

def test_generate_order_no(flash_order):
    order_no = generate_order_no(flash_order)
    assert isinstance(order_no, str)

def test_check_role_vendor(customer):
    with pytest.raises(PermissionDenied):
        assert check_role_vendor(customer) == False

def test_check_role_customer(customer):
    assert check_role_customer(customer) 

def test_get_role_url(customer):
    request = RequestFactory()
    request.user = customer
    assert get_role_url(request) == '/flash_sales/c/'
