import pytest 
from accounts.models import User, UserProfile
from vendor.models import Vendor, Product, OpeningHour

@pytest.fixture
def user(db):
    return User.objects.create(username='xiaoyao', email='a@gmail.com', role=2)

@pytest.fixture
def user_profile(db, user):
    return UserProfile.objects.get(user=user)

