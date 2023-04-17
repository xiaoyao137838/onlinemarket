from django.urls import reverse
from django.test import RequestFactory
from onlinemarket.views import home

def test_home(customer):
    path = reverse('home')
    request = RequestFactory().get(path)
    request.user = customer
    request.session = {}
    response = home(request)
    assert response.status_code == 200