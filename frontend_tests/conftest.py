import os
import socket
import pytest 
from selenium import webdriver
from pathlib import Path
from selenium.webdriver.chrome.service import Service


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