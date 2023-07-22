import os
import socket
import tempfile
from accounts.models import User, UserProfile
import pytest 
from selenium import webdriver
from pathlib import Path
from selenium.webdriver.chrome.service import Service
from vendor.models import Vendor
import logging

logger = logging.getLogger(__name__)

@pytest.fixture(scope='session')
def browser(request):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")

    BASE_DIR = Path(__file__).resolve().parent.parent
    driver_path = os.path.join(BASE_DIR, 'chromedriver.exe')
    ff_service = Service(executable_path=driver_path)
    browser = webdriver.Chrome(service=ff_service, options=options)

    def teardown():
        browser.quit()

    request.addfinalizer(teardown)
    return browser

# @pytest.fixture(scope='session')
# def base_url():
#     return f'http://{socket.gethostbyname(socket.gethostname())}:8000'

@pytest.fixture(scope='session')
def base_url():
    return f'http://localhost:8000'

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
