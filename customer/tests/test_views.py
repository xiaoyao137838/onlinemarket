from django.contrib.auth.models import AnonymousUser
from accounts.models import User
from django.test import RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer
from customer.views import customer_order, customer_profile, customer_orders
from accounts.views import customer_dashboard
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.messages.storage.fallback import FallbackStorage
from order.models import Order
from django.test import TestCase
import pytest
import json
import logging

logger = logging.getLogger(__name__)

def test_customer_dashboard_authenticated(user):

    path = reverse('customer')
    request = RequestFactory().get(path)
    request.user = user
    logger.info('user is : {}', user)

    response = customer_dashboard(request)
    assert response.status_code == 200

def test_customer_dashboard_unauthenticated():
    path = reverse('customer')
    request = RequestFactory().get(path)
    request.user = AnonymousUser()

    response = customer_dashboard(request)
    assert 'login' in response.url

def test_customer_profile_GET(user):
    path = reverse('customer_profile')
    request = RequestFactory().get(path)
    request.user = user

    response = customer_profile(request)
    assert response.status_code == 200

def test_customer_profile_POST(user):
    context = {
        'user_pic': SimpleUploadedFile("file.jpg", b"file_content"),
        'cover_photo': SimpleUploadedFile("file.jpg", b"file_content"),
        'address': 'new address',
        'email': 'cc@gmail.com'
    }
    path = reverse('customer_profile')
    request = RequestFactory().post(path, context)
    request.user = user

    setattr(request, 'session', 'session')
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)

    response = customer_profile(request)
    assert response.status_code == 302

def test_customer_profile_POST_invalid_form(user):
    context = {
        'user_pic': SimpleUploadedFile("file.pdf", b"file_content"),
        'cover_photo': SimpleUploadedFile("file.jpg", b"file_content"),
        'address': 'new address',
        'email': 'cc@gmail.com'
    }
    path = reverse('customer_profile')
    request = RequestFactory().post(path, context)
    request.user = user

    setattr(request, 'session', 'session')
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)

    response = customer_profile(request)
    assert response.status_code == 200

def test_customer_orders(user):
    path = reverse('customer_orders')
    request = RequestFactory().post(path)
    request.user = user

    response = customer_orders(request)
    assert response.status_code == 200

def test_customer_order_not_found(user):
    path = reverse('customer_order', args=[1])
    request = RequestFactory().get(path)
    request.user = user

    response = customer_order(request, 1)
    assert response.status_code == 302

def test_customer_order(user):
    order = Order.objects.create(
        order_no='test_order',
        sub_amount=10.0,
        tax_amount=0.0,
        total_amount=10.0,
        customer=user,
        status='Completed',
        tax_data=json.dumps({'Tax': {'0.07': 2.4}})
    )
    path = reverse('customer_order', args=[order.order_no])
    request = RequestFactory().get(path)
    request.user = user
    from order import models
    models.request_object = request 

    response = customer_order(request, order.order_no)
    assert response.status_code == 200
