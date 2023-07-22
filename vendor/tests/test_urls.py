from django.urls import reverse, resolve
from accounts.views import vendor_dashboard
from vendor.views import vendor_order, vendor_profile, vendor_orders, add_product, product, products, delete_product, opening_hours, add_opening_hour, delete_opening_hour
import logging

logger = logging.getLogger(__name__)

class TestUrls:
    def test_vendor_dashboard(self):
        path = reverse('vendor')
        logger.info('path is: %s', path)
        assert resolve(path).func == vendor_dashboard

    def test_vendor_profile(self):
        path = reverse('vendor_profile')
        logger.info('path is: %s', path)
        assert resolve(path).func == vendor_profile

    def test_vendor_orders(self):
        path = reverse('vendor_orders')
        logger.info('path is: %s', path)
        assert resolve(path).func == vendor_orders
    
    def test_vendor_order(self):
        path = reverse('vendor_order', args=[1])
        logger.info('path is: %s', path)
        assert resolve(path).func == vendor_order


    def test_products(self):
        path = reverse('products')
        logger.info('path is: %s', path)
        assert resolve(path).func == products
    
    def test_product(self):
        path = reverse('product', args=[1])
        logger.info('path is: %s', path)
        assert resolve(path).func == product

    def test_add_product(self):
        path = reverse('add_product')
        logger.info('path is: %s', path)
        assert resolve(path).func == add_product

    def test_detele_product(self):
        path = reverse('delete_product', args=[1])
        logger.info('path is: %s', path)
        assert resolve(path).func == delete_product

    
    def test_add_opening_hour(self):
        path = reverse('add_opening_hour')
        logger.info('path is: %s', path)
        assert resolve(path).func == add_opening_hour

    def test_opening_hours(self):
        path = reverse('opening_hours')
        logger.info('path is: %s', path)
        assert resolve(path).func == opening_hours

    def test_detele_opening_hour(self):
        path = reverse('delete_opening_hour', args=[1])
        logger.info('path is: %s', path)
        assert resolve(path).func == delete_opening_hour



