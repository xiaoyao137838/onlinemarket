from market.context_processors import get_cart_amounts, get_cart_counter, get_customer
from django.test import RequestFactory

def test_get_customer(customer):
    request = RequestFactory()
    request.user = customer
    assert get_customer(request) == customer

def test_get_cart_amounts(customer):
    request = RequestFactory()
    request.user = customer
    res = get_cart_amounts(request)
    assert isinstance(res, dict)

def test_get_cart_counter(customer):
    request = RequestFactory()
    request.user = customer
    res = get_cart_counter(request)
    assert isinstance(res, dict)