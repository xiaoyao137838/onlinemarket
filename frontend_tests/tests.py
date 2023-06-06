import os
from pathlib import Path
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.management import call_command
from django.urls import reverse

@pytest.mark.usefixtures('vendor')
class TestProjectListPage(StaticLiveServerTestCase):
    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")

        BASE_DIR = Path(__file__).resolve().parent.parent
        driver_path = os.path.join(BASE_DIR, 'chromedriver.exe')
        ff_service = Service(executable_path=driver_path)
        self.browser = webdriver.Chrome(service=ff_service, options=options)
        self.base_url = self.live_server_url

    def tearDown(self):
        self.browser.close()

    @pytest.mark.acceptance
    def test_homepage_displayed(self):
        print(self.browser)
        print(self.base_url)
        self.browser.get(self.base_url)
        title = self.browser.title
        content = self.browser.find_element(By.TAG_NAME, 'h1').text

        assert title == 'OnlineMarket'
        assert content == 'We Serve For Customers And Small Businesses!'

    @pytest.mark.acceptance
    def test_marketplace_displayed(self):
        marketplace_url = self.base_url + reverse('marketplace')
        self.browser.get(self.base_url)
        self.browser.find_element(By.LINK_TEXT, 'MARKET').click()
        current_url = self.browser.current_url

        assert marketplace_url == current_url

    @pytest.mark.acceptance
    def test_search(self):
        self.browser.get(self.base_url)
        keyword = self.browser.find_element(By.NAME, 'keyword')
        keyword.send_keys('fruit')
        address = self.browser.find_element(By.NAME, 'address')
        address.send_keys('279 Amherst R')
        radius = self.browser.find_element(By.NAME, 'radius')
        radius.send_keys(15)

        search_url = self.base_url + reverse('search')
        self.browser.find_element(By.XPATH, "//input[@value='Search']").click()
        current_url = self.browser.current_url
        assert search_url in current_url

