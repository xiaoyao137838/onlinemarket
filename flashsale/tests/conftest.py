import json
import tempfile
from flashsale.models import FlashOrder, FlashSale
import pytest 
from accounts.models import User, UserProfile
from order.models import Order, OrderedItem, Payment
from vendor.models import Product, Vendor
from datetime import datetime
from kafka.producer import KafkaProducer
from decouple import config
import redis
import logging

logger = logging.getLogger(__name__)

@pytest.fixture
def customer(db):
    return User.objects.create(id=18, username='customer_4', email='c4@gmail.com', role=2)

@pytest.fixture
def user(db):
    return User.objects.create(username='xiaoyao', email='a@gmail.com', role=1)

@pytest.fixture
def user_profile(db, user):
    profile = UserProfile.objects.get(user=user)
    profile.cover_photo = tempfile.NamedTemporaryFile(suffix=".jpg").name
    profile.user_pic = tempfile.NamedTemporaryFile(suffix=".jpg").name
    profile.save()
    return profile

@pytest.fixture
def vendor(db, user, user_profile):
    logger.info('db is:', db)
    return Vendor.objects.create(user=user, profile=user_profile, vendor_name='vendor_1', slug_name='slug')

@pytest.fixture
def product(db, vendor):
    return Product.objects.create(name='product_new', price=10, vendor=vendor, image=tempfile.NamedTemporaryFile(suffix=".jpg").name)

@pytest.fixture
def payment(db, customer):
    return Payment.objects.create(payment_no='pay_1', method='PayPal', customer=customer, amount=11.0, status='Completed')

@pytest.fixture
def flash_sale(db, product, customer, vendor):
    return FlashSale.objects.create(
        vendor = vendor,
        product = product,
        new_price = 10.0,
        total_qty = 10,
        to_time = datetime.now()
    )

@pytest.fixture
def flash_sale_redis(db, product, customer, vendor):
    return FlashSale.objects.create(
        vendor = vendor,
        product = product,
        new_price = 10.0,
        total_qty = 10,
        to_time = datetime.now()
    )

@pytest.fixture
def redis_cli():
    redis_cli = redis.Redis(config('REDIS_SERVER'))
    return redis_cli

@pytest.fixture
def flash_order(db, customer, payment, flash_sale, product):
    return FlashOrder.objects.create(product=product, first_name='geng', last_name='hong', order_no='order_1', customer=customer, sub_amount=10.0, tax_amount=1.0, tax_data=json.dumps({'tax': {'7': 1.0}}), total_amount=11.0, payment=payment, payment_method='PayPal', status=0, flash_sale=flash_sale)

@pytest.fixture
def producer():
    producer = KafkaProducer(bootstrap_servers=config('KAFKA_SERVER'))
    return producer