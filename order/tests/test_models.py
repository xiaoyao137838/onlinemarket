from django.test import RequestFactory

def test_payment_str(payment):
    assert str(payment) == payment.payment_no

def test_order_name(order):
    assert order.name == f'{order.first_name} {order.last_name}' 

def test_order_to_vendors(order):
    assert order.order_to_vendors() == ','.join([str(i) for i in order.vendors.all()]) 

def test_get_total_by_vendor(user, order, vendor):
    request = RequestFactory()
    request.user = user
    from order import models
    models.request_object = request 
    
    res = order.get_total_by_vendor()
    assert isinstance(res, dict)

def test_order_str(order):
    assert str(order) == order.order_no

def test_order_item_str(order_item):
    assert str(order_item) == order_item.product.name 