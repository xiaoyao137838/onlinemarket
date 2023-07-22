from django.urls import reverse, resolve
from accounts.views import dashboard, customer_dashboard, vendor_dashboard, register_user, register_vendor, login, logout, activate, password_reset_request, password_reset_validator, password_reset
import logging

logger = logging.getLogger(__name__)

class TestUrls:
    def test_account(self):
        path = reverse('account')
        assert resolve(path).func == dashboard

    def test_register_user(self):
        path = reverse('registerUser')
        assert resolve(path).func == register_user

    def test_register_vendor(self):
        path = reverse('registerVendor')
        assert resolve(path).func == register_vendor


    def test_login(self):
        path = reverse('login')
        assert resolve(path).func == login

    def test_logout(self):
        path = reverse('logout')
        assert resolve(path).func == logout

    def test_activate(self):
        path = reverse('activate', args=['user_id', 'test_token'])
        assert resolve(path).func == activate

    def test_password_reset_request(self):
        path = reverse('password_reset_request')
        assert resolve(path).func == password_reset_request

    def test_password_reset_validator(self):
        path = reverse('password_reset_validator', args=['user_id', 'test_token'])
        assert resolve(path).func == password_reset_validator

    def test_password_reset(self):
        path = reverse('password_reset')
        assert resolve(path).func == password_reset

    def test_dashboard(self):
        path = reverse('dashboard')
        logger.info('path is: %s', path)
        assert resolve(path).func == dashboard
    
    def test_customer_dashboard(self):
        path = reverse('customer_dashboard')
        logger.info('path is: %s', path)
        assert resolve(path).func == customer_dashboard

    def test_vendor_dashboard(self):
        path = reverse('vendor_dashboard')
        logger.info('path is: %s', path)
        assert resolve(path).func == vendor_dashboard


