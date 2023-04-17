import tempfile
import pytest 
from accounts.models import User, UserProfile
from order.models import Order, OrderedItem, Payment
from vendor.models import Product, Vendor

@pytest.fixture
def customer(db):
    return User.objects.create(username='customer_2', email='c@gmail.com', role=2)

@pytest.fixture
def user(db):
    return User.objects.create(username='xiaoyao', email='a@gmail.com', role=1)

@pytest.fixture
def user_profile(db, user):
    return UserProfile.objects.get(user=user)

@pytest.fixture
def vendor(db, user, user_profile):
    print('db is:', db)
    return Vendor.objects.create(user=user, profile=user_profile, vendor_name='vendor_1', slug_name='slug')

@pytest.fixture
def product(db, vendor):
    return Product.objects.create(name='product_new', price=10, vendor=vendor, image=tempfile.NamedTemporaryFile(suffix=".jpg").name)

@pytest.fixture
def payment(db, customer):
    return Payment.objects.create(payment_no='pay_1', method='PayPal', customer=customer, amount=11.0, status='Completed')

@pytest.fixture
def order(db, customer, payment):
    return Order.objects.create(first_name='geng', last_name='hong', order_no='order_1', customer=customer, sub_amount=10.0, tax_amount=1.0, total_amount=11.0, payment=payment, status='Completed')

@pytest.fixture
def order_item(db, product, customer, order):
    return OrderedItem.objects.create(
        product = product,
        price = 10.0,
        quantity = 1,
        amount = 10.0,
        customer = customer,
        order = order
    )