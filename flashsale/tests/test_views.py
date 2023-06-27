from datetime import datetime
from django.urls import reverse
from django.test import RequestFactory
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.messages.storage.fallback import FallbackStorage
from flashsale.views import add_flashsale, delete_flashsale, flashsale, flashsale_customer, flashsale_vendor, flashsales, make_payment, select_flash_sale, checkout, make_order, pay_done, get_vendor
from flashsale.models import FlashOrder
from django.contrib.auth.models import AnonymousUser
import logging

logger = logging.getLogger(__name__)

def test_get_vendor(user, vendor):
    request = RequestFactory()
    request.user = user
    assert vendor == get_vendor(request)

def test_flashsales(user, vendor):
    path = reverse('flashsales', args=[vendor.slug_name])
    request = RequestFactory().get(path)
    request.user = user
    response = flashsales(request, vendor.slug_name)
    assert response.status_code == 200

def test_add_flashsale_GET(user, vendor, product):
    path = reverse('add_flashsale', args=[product.id])
    request = RequestFactory().get(path)
    request.user = user
    response = add_flashsale(request, product.id)
    assert response.status_code == 200

def test_add_flashsale_POST(user, vendor, product):
    path = reverse('add_flashsale', args=[product.id])
    request = RequestFactory().post(path)
    request.user = user
    request.POST = {
            'new_price': 10.0,
            'to_time': datetime.now(),
            'total_qty': 10,
            'available_qty': 0
    }

    setattr(request, 'session', 'session')
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)    

    response = add_flashsale(request, product.id)
    assert response.status_code == 302

def test_add_flashsale_POST_invalid_form(user, vendor, product):
    path = reverse('add_flashsale', args=[product.id])
    request = RequestFactory().post(path)
    request.user = user
    request.POST = {
            'new_price': 10.0,
            'to_time': datetime.now(),
            'available_qty': 0
    }

    setattr(request, 'session', 'session')
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)    

    response = add_flashsale(request, product.id)
    assert response.status_code == 200

def test_delete_flashsale(user, vendor, flash_sale):
    path = reverse('delete_flashsale', args=[flash_sale.id])
    request = RequestFactory().get(path)
    request.user = user
    logger.info('flash id: {}', flash_sale)

    setattr(request, 'session', 'session')
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages) 

    response = delete_flashsale(request, flash_sale.id)
    assert response.status_code == 302

def test_flashsale(user, vendor, flash_sale):
    path = reverse('flashsale', args=[flash_sale.id])
    request = RequestFactory().get(path)
    request.user = user

    response = flashsale(request, flash_sale.id)
    assert response.status_code == 302

def test_flashsale_customer(customer, vendor, flash_sale):
    path = reverse('flashsale_customer', args=[flash_sale.id])
    request = RequestFactory().get(path)
    request.user = customer
    
    response = flashsale_customer(request, flash_sale.id)
    assert response.status_code == 200

def test_flashsale_vendor_GET(user, vendor, flash_sale):
    path = reverse('flashsale_vendor', args=[flash_sale.id])
    request = RequestFactory().get(path)
    request.user = user
    
    response = flashsale_vendor(request, flash_sale.id)
    assert response.status_code == 200

def test_flashsale_vendor_POST(user, vendor, flash_sale):
    context = {
        'new_price': 10.0,
        'to_time': datetime.now(),
        'total_qty': 10,
        'available_qty': 0
    }
    path = reverse('flashsale_vendor', args=[flash_sale.id])
    request = RequestFactory().post(path, context)
    request.user = user

    setattr(request, 'session', 'session')
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages) 
    
    response = flashsale_vendor(request, flash_sale.id)
    assert response.status_code == 302

def test_flashsale_vendor_POST_invalid_form(user, vendor, flash_sale):
    context = {
        'new_price': 10.0,
        'to_time': datetime.now(),
        'available_qty': 0
    }
    path = reverse('flashsale_vendor', args=[flash_sale.id])
    request = RequestFactory().post(path, context)
    request.user = user

    setattr(request, 'session', 'session')
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages) 
    
    response = flashsale_vendor(request, flash_sale.id)
    assert response.status_code == 200

def test_select_flash_sale(customer, flash_sale_redis):
    path = reverse('flash_select')
    request = RequestFactory().get(path)

    request.user = AnonymousUser()
    response = select_flash_sale(request)
    assert response.status_code == 302

    request.user = customer
    request.GET = {
        'flash_sale_id': flash_sale_redis.id
    }
    response = select_flash_sale(request)
    assert response.status_code == 200
    
    request.headers = {}
    request.headers['x-requested-with'] = 'XMLHttpRequest'
    
    response = select_flash_sale(request)
    assert response.status_code == 200

def test_checkout(flash_sale, customer, flash_order, vendor):
    path = reverse('flash_checkout', args=[flash_sale.id])
    request = RequestFactory().get(path)
    request.user = customer
    
    response = checkout(request, flash_sale.id)
    assert response.status_code == 200

def test_make_order_POST(flash_sale, customer, payment, flash_order):
    context = {
        'first_name': 'geng', 
        'last_name': 'hong', 
        'order_no': 'order_1', 
        'customer': customer, 
        'sub_amount': 10.0, 
        'tax_amount': 1.0, 
        'total_amount': 11.0, 
        'payment': payment, 
        'payment_method': 'PayPal', 
        'status': 0, 
        'flash_sale': flash_sale
    }
    path = reverse('flash_make_order', args=[flash_sale.id])
    request = RequestFactory().post(path, context)
    request.user = customer
    
    response = make_order(request, flash_sale.id)
    assert response.status_code == 200

def test_make_payment_POST(customer, flash_sale, flash_order, producer):
    path = reverse('flash_make_payment')
    request = RequestFactory().post(path)
    request.user = customer
    request.POST = {
        'transaction_id': 'transac_id',
        'sale_order_no': flash_order.order_no,
        'payment_method': 'PayPal'
    }
    
    request.headers = {}
    request.headers['x-requested-with'] = 'XMLHttpRequest'
    
    response = make_payment(request)
    assert response.status_code == 200

def test_pay_done(customer, flash_order, payment):
    path = reverse('flash_pay_done')
    request = RequestFactory().get(path)
    request.user = customer
    request.GET = {
        'sale_order_no': 'order_1',
        'trans_id': 'pay_1'
    }
    response = pay_done(request)
    assert response.status_code == 200

    