from django.urls import reverse, resolve
from customer.views import customer_profile, customer_order, customer_orders
from accounts.views import customer_dashboard

class TestUrls:
    def test_customer_dashboard(self):
        path = reverse('customer')
        assert resolve(path).func == customer_dashboard

    def test_customer_profile(self):
        path = reverse('customer_profile')
        print('path is: ', path)
        assert resolve(path).func == customer_profile

    def test_customer_orders(self):
        path = reverse('customer_orders')
        print('path is: ', path)
        assert resolve(path).func == customer_orders
    
    def test_customer_order(self):
        path = reverse('customer_order', args=[1])
        print('path is: ', path)
        assert resolve(path).func == customer_order
