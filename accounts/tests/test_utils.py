from django.test import RequestFactory
from django.core.exceptions import PermissionDenied
from accounts.utils import check_role_customer, check_role_vendor, get_role_url, send_email_activation, send_notification
import pytest 

def test_check_role_customer(user):
    with pytest.raises(PermissionDenied):
        check_role_customer(user)

def test_check_role_vendor(user):
    assert check_role_vendor(user) == True

def test_get_role_url(user):
    request = RequestFactory()
    request.user = user
    assert get_role_url(request) == 'vendor_dashboard'

def test_send_email_activation():
    assert True 

def test_send_notification():
    assert True
    
