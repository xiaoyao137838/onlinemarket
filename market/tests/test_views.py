from market.views import marketplace, vendor_detail, add_cart, deduce_cart, remove_cart
from django.urls import reverse
from django.test import RequestFactory
from market.models import CartItem
import logging

logger = logging.getLogger(__name__)

def test_marketplace(customer):
    path = reverse('marketplace')
    request = RequestFactory().get(path)
    request.user = customer
    response = marketplace(request)
    assert response.status_code == 200

def test_vendor_detail(customer, vendor):
    path = reverse('vendor_detail', args=[vendor.slug_name])
    request = RequestFactory().get(path)
    request.user = customer
    response = vendor_detail(request, vendor.slug_name)
    assert response.status_code == 200

def test_add_cart(customer, product):
    pre_count = CartItem.objects.count()
    path = reverse('add_cart', args=[product.id])
    request = RequestFactory().get(path)
    request.user = customer
    request.headers = {}
    request.headers['x-requested-with'] = 'XMLHttpRequest'

    response = add_cart(request, product.id)
    post_count = CartItem.objects.count()
    assert response.status_code == 200
    assert post_count - pre_count == 1

def test_deduce_cart(customer, cart_item, product):
    logger.info('cart item quantity is {}', cart_item.quantity)
    pre_count = cart_item.quantity
    path = reverse('deduce_cart', args=[product.id])
    request = RequestFactory().get(path)
    request.user = customer
    request.headers = {}
    request.headers['x-requested-with'] = 'XMLHttpRequest'

    response = deduce_cart(request, product.id)
    post_count = CartItem.objects.get(product=product).quantity
    assert response.status_code == 200
    assert pre_count - post_count == 1

def test_remove_cart(customer, cart_item, product):
    pre_count = CartItem.objects.count()
    path = reverse('add_cart', args=[cart_item.id])
    request = RequestFactory().get(path)
    request.user = customer
    request.headers = {}
    request.headers['x-requested-with'] = 'XMLHttpRequest'

    response = remove_cart(request, cart_item.id)
    post_count = CartItem.objects.count()
    logger.info('pre count is {}, post count is {}', pre_count, post_count)
    assert response.status_code == 200
    assert post_count == 0