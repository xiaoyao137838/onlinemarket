from django.urls import reverse
from django.test import RequestFactory
from order.views import place_order, make_payment, payment_complete

def test_place_order_GET(customer):
    path = reverse('place_order')
    request = RequestFactory().get(path)
    request.user = customer
    response = place_order(request)
    assert response.status_code == 302

def test_place_order_POST(customer):
    path = reverse('place_order')
    request = RequestFactory().post(path)
    request.user = customer
    request.POST = {
        'payment_method': 'PayPal'
    }
    response = place_order(request)
    assert response.status_code == 200

def test_make_payment_POST(customer, order):
    path = reverse('make_payment')
    request = RequestFactory().post(path)
    request.user = customer
  
    request.POST = {
        'payment_method': 'PayPal',
        'order_no': '1111111xxx',
        'transaction_id': 'xxxx111',
        'status': 'New'
    }
    response = make_payment(request)
    assert response.status_code == 200

def test_payment_complete(customer, order, order_item):
    path = reverse('payment_complete')
    request = RequestFactory().post(path)
    request.user = customer

    request.GET = {
        'order_no': 'order_1',
        'trans_id': 'pay_1',
    }
    response = payment_complete(request)
    assert response.status_code == 200