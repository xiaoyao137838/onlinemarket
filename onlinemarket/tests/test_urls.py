import pytest
from onlinemarket.views import home
from market.views import cart, checkout, search
from django.urls import reverse, resolve

class TestUrls:
    def test_home(self):
        path = reverse('home')
        print('path is: ', path)
        assert resolve(path).func == home

    def test_cart(self):
        path = reverse('cart')
        print('path is: ', path)
        assert resolve(path).func == cart
    
    def test_checkout(self):
        path = reverse('checkout')
        print('path is: ', path)
        assert resolve(path).func == checkout

    def test_search(self):
        path = reverse('search')
        print('path is: ', path)
        assert resolve(path).func == search