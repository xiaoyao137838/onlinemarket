import pytest 
from accounts.models import User

@pytest.fixture
def customer(db):
    return User.objects.create(username='customer_2', email='c@gmail.com', role=2)