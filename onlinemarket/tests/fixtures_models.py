import pytest 
from accounts.models import User, UserProfile
from vendor.models import Vendor

@pytest.fixture
def c_user_test(scope="function"):
    user = User.objects.create_user(username='c_user_test', email='c_user_test@gmail.com', password='111111')
    return user

@pytest.fixture
def v_user_test(scope="function"):
    user = User.objects.create_user(username='v_user_test', email='v_user_test@gmail.com', password='111111')
    return user

@pytest.fixture
def user_admin_test(scope="function"):
    admin = User.objects.create_superuser(username='admin_test', email='admin_test@gmail.com', password='111111')
    return admin 

@pytest.fixture
def c_profile_test(scope="function"):
    c_profile_test = UserProfile.objects.create(user=c_user_test)
    return c_profile_test 

@pytest.fixture
def v_profile_test(scope="function"):
    v_profile_test = UserProfile.objects.create(user=v_user_test)
    return v_profile_test 

@pytest.fixture
def vendor_test(scope="function"):
    vendor_test = Vendor.objects.create(user=v_user_test, profile=v_profile_test, vendor_name='vendor_test', slug_name='vendor_test', is_verified=True, verified_file='verify.png')
    return vendor_test