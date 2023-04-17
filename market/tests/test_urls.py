from django.urls import reverse, resolve
from market.views import marketplace, vendor_detail, add_cart, deduce_cart, remove_cart

class TestUrls:
    def test_marketplace(self):
        path = reverse('marketplace')
        print('path is: ', path)
        assert resolve(path).func == marketplace

    def test_vendor_detail(self):
        path = reverse('vendor_detail', args=['slug-name'])
        print('path is: ', path)
        assert resolve(path).func == vendor_detail

    def test_add_cart(self):
        path = reverse('add_cart', args=[1])
        assert resolve(path).func == add_cart
        
    def test_deduce_cart(self):
        path = reverse('deduce_cart', args=[1])
        assert resolve(path).func == deduce_cart
        
    def test_remove_cart(self):
        path = reverse('remove_cart', args=[1])
        assert resolve(path).func == remove_cart