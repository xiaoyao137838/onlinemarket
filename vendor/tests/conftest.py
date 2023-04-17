import pytest 
from accounts.models import User, UserProfile
from vendor.models import Vendor, Product, OpeningHour
import tempfile

@pytest.fixture
def user(db):
    return User.objects.create(username='xiaoyao', email='a@gmail.com', role=1)

@pytest.fixture
def user_profile(db, user):
    return UserProfile.objects.get(user=user)

@pytest.fixture
def vendor(db, user, user_profile):
    print('db is:', db)
    return Vendor.objects.create(user=user, profile=user_profile, vendor_name='vendor_1', verified_file=tempfile.NamedTemporaryFile(suffix=".jpg").name, slug_name='vendor_1')


@pytest.fixture(scope='function')
def product(db, vendor):
    product = Product.objects.create(name='product_1', price=10, vendor=vendor, image=tempfile.NamedTemporaryFile(suffix=".jpg").name)
    print('product image: ', product.image)
    return product

@pytest.fixture(scope='function')
def opening_hour(db,vendor):
    return OpeningHour.objects.create(day=1, vendor=vendor)