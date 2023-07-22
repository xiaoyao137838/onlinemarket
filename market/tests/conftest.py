import tempfile
from vendor.models import Product
from accounts.models import User, UserProfile
from vendor.models import Vendor
from market.models import CartItem, Tax
import pytest 
import logging

logger = logging.getLogger(__name__)

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
    logger.info('db is: %s', db)
    return Vendor.objects.create(user=user, profile=user_profile, vendor_name='vendor_1', slug_name='vendor_1')

@pytest.fixture(scope='function')
def product(db, vendor):
    return Product.objects.create(name='product_2', price=10, vendor=vendor)

@pytest.fixture
def customer(db):
    return User.objects.create(username='customer_2', email='c@gmail.com', role=2)

@pytest.fixture
def cart_item(db, product, customer):
    return CartItem.objects.create(product=product, customer=customer, quantity=3)

@pytest.fixture
def tax(db):
    return Tax.objects.create(tax_type='tax', percentage=7)