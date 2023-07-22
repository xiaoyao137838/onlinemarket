import pytest
from order.views import place_order, make_payment, payment_complete
from django.urls import reverse, resolve
import logging

logger = logging.getLogger(__name__)

class TestUrls:
    def test_place_order(self):
        path = reverse('place_order')
        logger.info('path is: %s', path)
        assert resolve(path).func == place_order

    def test_make_payment(self):
        path = reverse('make_payment')
        logger.info('path is: %s', path)
        assert resolve(path).func == make_payment
    
    def test_payment_complete(self):
        path = reverse('payment_complete')
        logger.info('path is: %s', path)
        assert resolve(path).func == payment_complete

