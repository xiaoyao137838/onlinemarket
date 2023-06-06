from base64 import urlsafe_b64encode
from django.urls import reverse, resolve
from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.messages.storage.fallback import FallbackStorage
from accounts.views import dashboard, customer_dashboard, vendor_dashboard, register_user, register_vendor, login, logout, activate, password_reset_request, password_reset_validator, password_reset
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sessions.middleware import SessionMiddleware
from order.models import Order
import pytest

def test_account(user):
    path = reverse('account')
    request = RequestFactory().get(path)
    request.user = user
    response = dashboard(request)
    assert response.status_code == 302

def test_register_user_already_login(user):
    path = reverse('registerUser')
    request = RequestFactory().get(path)
    request.user = user

    setattr(request, 'session', 'session')
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)

    response = register_user(request)
    assert response.status_code == 302

def test_register_user_GET():
    path = reverse('registerUser')
    request = RequestFactory().get(path)
    request.user = AnonymousUser()
    response = register_user(request)
    assert response.status_code == 200

def test_register_user_POST(db):
    path = reverse('registerUser')
    request = RequestFactory().post(path)
    request.user = AnonymousUser()
    request.POST = {
        'username': 'new_user',
        'email': 'WW@gmail.com',
        'password': '111111',
        'confirm_password': '111111'
    }

    setattr(request, 'session', 'session')
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)

    response = register_user(request)
    assert response.status_code == 302

def test_register_user_POST_invalid_form(db):
    path = reverse('registerUser')
    request = RequestFactory().post(path)
    request.user = AnonymousUser()
    request.POST = {
        'email': 'WW@gmail.com',
        'password': '111111',
        'confirm_password': '111111'
    }
    response = register_user(request)
    assert response.status_code == 200

def test_register_vendor_already_login(user):
    path = reverse('registerVendor')
    request = RequestFactory().get(path)
    request.user = user

    setattr(request, 'session', 'session')
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)

    response = register_user(request)
    assert response.status_code == 302

def test_register_vendor_GET():
    path = reverse('registerVendor')
    request = RequestFactory().get(path)
    request.user = AnonymousUser()
    response = register_vendor(request)
    assert response.status_code == 200

def test_register_vendor_POST(db):
    context = {
        'username': 'new_user',
        'email': 'WW@gmail.com',
        'password': '111111',
        'confirm_password': '111111',
        'vendor_name': 'new v',
        'verified_file': SimpleUploadedFile("file.jpg", b"file_content"),
    }
    path = reverse('registerVendor')
    request = RequestFactory().post(path, context)
    request.user = AnonymousUser()

    setattr(request, 'session', 'session')
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)

    response = register_vendor(request)
    assert response.status_code == 302

def test_register_vendor_POST_invalid_form(db):
    context = {
        'email': 'WW@gmail.com',
        'password': '111111',
        'confirm_password': '111111',
        'vendor_name': 'new v',
        'verified_file': SimpleUploadedFile("file.jpg", b"file_content"),
    }
    path = reverse('registerVendor')
    request = RequestFactory().post(path, context)
    request.user = AnonymousUser()

    setattr(request, 'session', 'session')
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)

    response = register_vendor(request)
    assert response.status_code == 200

def test_login_already_login(user):
    path = reverse('login')
    request = RequestFactory().get(path)
    request.user = user

    setattr(request, 'session', 'session')
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)

    response = login(request)
    assert response.status_code == 302

def test_login_GET():
    path = reverse('login')
    request = RequestFactory().get(path)
    request.user = AnonymousUser()
    response = login(request)
    assert response.status_code == 200

def test_login_POST(user):
    path = reverse('login')
    request = RequestFactory().post(path)
    request.user = AnonymousUser()
    request.POST = {
        'username': 'xiaoyao',
        'password': '111111'
    }
    setattr(request, 'session', 'session')
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)

    response = login(request)
    assert response.status_code == 302

def test_logout(user):
    path = reverse('logout')
    request = RequestFactory().get(path)
    request.user = user

    sm = SessionMiddleware(lambda req: print(req))
    sm.process_request(request)
    
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)

    response = logout(request)
    assert response.status_code == 302

def test_activate(user):
    uidb64 = urlsafe_b64encode(force_bytes(user.id))
    token = default_token_generator.make_token(user)
     
    path = reverse('activate', kwargs={ 'uidb64': uidb64, 'token': token })
    request = RequestFactory().get(path)
    request.user = AnonymousUser()

    setattr(request, 'session', 'session')
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)

    # response = activate(request, uidb64, token)
    # assert response.status_code == 302

def test_password_reset_request_GET(user):
    path = reverse('password_reset_request')
    request = RequestFactory().get(path)
    request.user = AnonymousUser()

    setattr(request, 'session', 'session')
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)

    response = password_reset_request(request)
    assert response.status_code == 200

def test_password_reset_request_POST(user):
    path = reverse('password_reset_request')
    request = RequestFactory().post(path)
    request.user = AnonymousUser()
    request.POST = {
        'username': user.username
    }

    setattr(request, 'session', 'session')
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)

    response = password_reset_request(request)
    assert response.status_code == 302

def test_password_reset_request_POST_no_user(user):
    path = reverse('password_reset_request')
    request = RequestFactory().post(path)
    request.user = AnonymousUser()
    request.POST = {
        'username': 'xx'
    }

    setattr(request, 'session', 'session')
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)

    response = password_reset_request(request)
    assert response.status_code == 200

def test_password_reset_validator(user):
    uidb64 = urlsafe_b64encode(force_bytes(user.id))
    token = default_token_generator.make_token(user)
     
    path = reverse('password_reset_validator', kwargs={ 'uid': uidb64, 'token': token })
    request = RequestFactory().get(path)
    request.user = AnonymousUser()

    setattr(request, 'session', 'session')
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)
    # response = password_reset_validator(request, uidb64, token)
    # assert response.status_code == 302

def test_password_reset_GET(user):
    path = reverse('password_reset')
    request = RequestFactory().get(path)
    request.user = AnonymousUser()

    setattr(request, 'session', 'session')
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)

    response = password_reset(request)
    assert response.status_code == 200

def test_password_reset_POST(user):
    path = reverse('password_reset')
    request = RequestFactory().post(path)
    request.user = AnonymousUser()
    request.POST = {
        'password': '111111',
        'confirm_password': '111111'
    }
    request.session = {}
    request.session["uid"]= int(user.id)

    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)

    response = password_reset(request)
    assert response.status_code == 302

def test_password_reset_POST_dismatch_password(user):
    path = reverse('password_reset')
    request = RequestFactory().post(path)
    request.user = AnonymousUser()
    request.POST = {
        'password': '111111',
        'confirm_password': '211111'
    }
    request.session = {}
    request.session["uid"]= int(user.id)

    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)

    response = password_reset(request)
    assert response.status_code == 200

def test_dashboard(user):
    path = reverse('dashboard')
    request = RequestFactory().get(path)
    request.user = user
    response = dashboard(request)
    assert response.status_code == 302

def test_customer_dashboard(customer):
    path = reverse('customer_dashboard')
    request = RequestFactory().get(path)
    request.user = customer
    response = dashboard(request)
    assert response.status_code == 302

def test_vendor_dashboard(user, vendor, order):
    path = reverse('vendor_dashboard')
    request = RequestFactory().get(path)
    request.user = user
    response = dashboard(request)
    assert response.status_code == 302

    vendors = set({})
    vendors.add(vendor)
    order.vendors.set(vendors)
    order.save()
    orders = Order.objects.filter(status='Completed', vendors__in=[vendor]).order_by('-created_at') 
    assert orders.count() == 1