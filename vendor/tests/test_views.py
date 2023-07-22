import tempfile
from django.contrib.auth.models import AnonymousUser
from accounts.models import User
from django.test import RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer
from vendor.views import vendor_order, vendor_profile, vendor_orders, add_product, product, products, delete_product, opening_hours, add_opening_hour, delete_opening_hour
from accounts.views import vendor_dashboard
from order.models import Order
from vendor. models import OpeningHour
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.messages.storage.fallback import FallbackStorage
import pytest
import json
import logging

logger = logging.getLogger(__name__)

def test_vendor_dashboard_authenticated(user, vendor):

    path = reverse('vendor')
    request = RequestFactory().get(path)
    request.user = user
    logger.info('user is : %s', user)

    response = vendor_dashboard(request)
    assert response.status_code == 200

def test_vendor_dashboard_unauthenticated():
    path = reverse('vendor')
    request = RequestFactory().get(path)
    request.user = AnonymousUser()

    response = vendor_dashboard(request)
    assert 'login' in response.url

def test_vendor_profile_GET(user, vendor):
    path = reverse('vendor_profile')
    request = RequestFactory().get(path)
    request.user = user

    response = vendor_profile(request)
    assert response.status_code == 200

def test_vendor_profile_POST(user, vendor):
    context = {
        'verified_file': SimpleUploadedFile("file.jpg", b"file_content"),
        'user_pic': SimpleUploadedFile("file.jpg", b"file_content"),
        'cover_photo': SimpleUploadedFile("file.jpg", b"file_content"),
        'address': 'new address',
        'vendor_name': 'vender_1'
    }
    path = reverse('vendor_profile')
    request = RequestFactory().post(path, context)
    request.user = user
    
    setattr(request, 'session', 'session')
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)

    response = vendor_profile(request)
    assert response.status_code == 302

def test_vendor_orders(user, vendor):
    path = reverse('vendor_orders')
    request = RequestFactory().get(path)
    request.user = user

    response = vendor_orders(request)
    assert response.status_code == 200

def test_vendor_order_not_found(user, vendor):
    path = reverse('vendor_order', args=[1])
    request = RequestFactory().get(path)
    request.user = user

    response = vendor_order(request, 1)
    assert response.status_code == 302

def test_vendor_order(user, vendor):
    order = Order.objects.create(
        order_no='test_order',
        sub_amount=10.0,
        tax_amount=0.0,
        total_amount=10.0,
    )
    path = reverse('vendor_order', args=[order.order_no])
    request = RequestFactory().get(path)
    request.user = user
    from order import models
    models.request_object = request 

    response = vendor_order(request, order.order_no)
    assert response.status_code == 200

def test_products(user, vendor):
    path = reverse('products')
    request = RequestFactory().get(path)
    request.user = user 
    response = products(request)
    assert response.status_code == 200

def test_add_product_GET(user, vendor):
    path = reverse('add_product')
    request = RequestFactory().get(path)
    request.user = user 
    response = add_product(request)
    assert response.status_code == 200

def test_add_product_POST(user, vendor):
    context = {
        'image': SimpleUploadedFile("file.jpg", b"file_content"),
        'name': 'product_4',
        'price': 22
    }
    path = reverse('add_product')
    request = RequestFactory().post(path, context)
    request.user = user 

    setattr(request, 'session', 'session')
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)

    response = add_product(request)
    assert response.status_code == 302

def test_product_GET(user, vendor, product):
    path = reverse('product', args=[product.id])
    request = RequestFactory().get(path)
    request.user = user
    from vendor import views
    response = views.product(request, product.id)
    assert response.status_code == 200

def test_product_POST(user, vendor, product):
    context = {
        'image': SimpleUploadedFile("file.jpg", b"file_content"),
        'name': 'product_4',
        'price': 22
    }
    path = reverse('product', args=[product.id])
    request = RequestFactory().post(path, context)
    request.user = user

    setattr(request, 'session', 'session')
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)

    from vendor import views
    response = views.product(request, product.id)
    assert response.status_code == 302


def test_delete_product(user, vendor, product):
    path = reverse('delete_product', args=[product.id])
    request = RequestFactory().get(path)
    request.user = user
    setattr(request, 'session', 'session')
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)

    response = delete_product(request, product.id)
    assert response.status_code == 302

def test_opening_hours(user, vendor, opening_hour):
    path = reverse('opening_hours')
    request = RequestFactory().get(path)
    request.user = user 
    response = opening_hours(request)
    assert response.status_code == 200

def test_add_opening_hour(user, vendor, opening_hour):
    context = {
        'day': 3,
        'from_time': 'from',
        'to_time': 'to',
        'is_closed': True
    }
    pre_count = OpeningHour.objects.count()
    path = reverse('add_opening_hour')
    request = RequestFactory().post(path, context)
    request.user = user 
    request.headers = {}
    request.headers['x-requested-with'] = 'XMLHttpRequest'

    response = add_opening_hour(request)
    post_count = OpeningHour.objects.count()
    assert response.status_code == 200
    assert post_count - pre_count == 1

def test_delete_opening_hour(user, vendor, opening_hour):
    pre_count = OpeningHour.objects.count()
    path = reverse('delete_opening_hour', args=[opening_hour.id])
    request = RequestFactory().get(path)
    request.user = user 
    request.headers = {}
    request.headers['x-requested-with'] = 'XMLHttpRequest'
    
    response = delete_opening_hour(request, opening_hour.id)
    post_count = OpeningHour.objects.count()
    assert response.status_code == 200
    assert pre_count - 1 == post_count