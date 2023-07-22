import pytest
from flashsale.views import add_flashsale, delete_flashsale, flashsale, flashsale_customer, flashsale_vendor, flashsales, make_payment, select_flash_sale, checkout, make_order, pay_done
from django.urls import reverse, resolve
import logging

logger = logging.getLogger(__name__)

class TestUrls:
    def test_flashsales(self):
        path = reverse('flashsales', args=['slug'])
        assert resolve(path).func == flashsales

    def test_add_flashsale(self):
        path = reverse('add_flashsale', args=[1])
        assert resolve(path).func == add_flashsale

    def test_delete_flashsale(self):
        path = reverse('delete_flashsale', args=[1])
        assert resolve(path).func == delete_flashsale

    def test_flashsale(self):
        path = reverse('flashsale', args=[1])
        assert resolve(path).func == flashsale

    def test_flashsale_customer(self):
        path = reverse('flashsale_customer', args=[1])
        assert resolve(path).func == flashsale_customer

    def test_flashsale_vendor(self):
        path = reverse('flashsale_vendor', args=[1])
        assert resolve(path).func == flashsale_vendor

    def test_flash_select(self):
        path = reverse('flash_select')
        assert resolve(path).func == select_flash_sale

    def test_flash_checkout(self):
        path = reverse('flash_checkout', args=[1])
        assert resolve(path).func == checkout

    def test_flash_make_order(self):
        path = reverse('flash_make_order', args=[1])
        logger.info('path is: %s', path)
        assert resolve(path).func == make_order

    def test_flash_make_payment(self):
        path = reverse('flash_make_payment')
        logger.info('path is: %s', path)
        assert resolve(path).func == make_payment
    
    def test_flash_pay_done(self):
        path = reverse('flash_pay_done')
        logger.info('path is: %s', path)
        assert resolve(path).func == pay_done

