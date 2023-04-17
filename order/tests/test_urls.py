import pytest
from order.views import place_order, make_payment, payment_complete
from django.urls import reverse, resolve

class TestUrls:
    def test_place_order(self):
        path = reverse('place_order')
        print('path is: ', path)
        assert resolve(path).func == place_order

    def test_make_payment(self):
        path = reverse('make_payment')
        print('path is: ', path)
        assert resolve(path).func == make_payment
    
    def test_payment_complete(self):
        path = reverse('payment_complete')
        print('path is: ', path)
        assert resolve(path).func == payment_complete

