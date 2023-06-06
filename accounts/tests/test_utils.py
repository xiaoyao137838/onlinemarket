from django.test import RequestFactory
from django.core.exceptions import PermissionDenied
from accounts.utils import check_role_customer, check_role_vendor, get_role_url, send_email_activation, send_notification
import pytest 

def test_check_role_customer(user):
    with pytest.raises(PermissionDenied):
        check_role_customer(user)

def test_check_role_vendor(user):
    assert check_role_vendor(user) == True
    user.role = 2
    user.save()
    with pytest.raises(PermissionDenied):
        check_role_vendor(user)

def test_get_role_url(user):
    request = RequestFactory()
    request.user = user
    assert get_role_url(request) == 'vendor_dashboard'

    user.role = 2
    user.save()
    assert get_role_url(request) == 'customer_dashboard'

    user.role = 0
    user.is_admin = True
    user.save()
    assert get_role_url(request) == '/admin'

def test_send_email_activation(user):
    request = RequestFactory()
    request.user = user
    request.get_host = lambda : '/'
    send_email_activation(request, user,'acitvation subject', 'emails/email_activation.html')
    assert True 

def test_send_notification_single(user):
    request = RequestFactory()
    request.user = user
    context = {
        'to_email': 'to@gmail.com'
    }
    send_notification('notification subject', 'order/customer_order_email.html', context)
    assert True
    
def test_send_notification_array(user):
    request = RequestFactory()
    request.user = user
    context = {
        'to_email': ['to@gmail.com']
    }
    send_notification('notification subject', 'order/customer_order_email.html', context)
    assert True
    
