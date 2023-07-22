from order.models import Order, Payment
import pytest 
from accounts.models import User, UserProfile
from vendor.models import Vendor, Product, OpeningHour
from onlinemarket import settings
from django.contrib import messages, auth
import logging

logger = logging.getLogger(__name__)

@pytest.fixture
def user(db):
    return User.objects.create(username='xiaoyao', email='a@gmail.com', role=1, password='111111')

@pytest.fixture
def user_profile(db, user):
    return UserProfile.objects.get(user=user)

@pytest.fixture
def vendor(db, user, user_profile):
    logger.info('db is: %s', db)
    return Vendor.objects.create(user=user, profile=user_profile, vendor_name='vendor_1')

@pytest.fixture
def customer(db):
    return User.objects.create(username='customer_test', email='c@gmail.com', role=2)

@pytest.fixture(scope='function')
def product(db, vendor):
    return Product.objects.create(name='product_1', price=10, vendor=vendor)

@pytest.fixture(scope='function')
def opening_hour(db,vendor):
    return OpeningHour.objects.create(day=1, vendor=vendor)

@pytest.fixture
def payment(db, customer):
    return Payment.objects.create(payment_no='pay_1', method='PayPal', customer=customer, amount=11.0, status='Completed')

@pytest.fixture
def order(db, customer, payment):
    return Order.objects.create(first_name='geng', last_name='hong', order_no='order_1', customer=customer, sub_amount=10.0, tax_amount=1.0, total_amount=11.0, payment=payment, status='Completed')