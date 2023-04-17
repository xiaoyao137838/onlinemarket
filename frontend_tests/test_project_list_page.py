import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse

@pytest.mark.acceptance
def test_homepage_displayed(browser, base_url):
    print(browser)
    print(base_url)
    browser.get(base_url)
    title = browser.title
    content = browser.find_element(By.TAG_NAME, 'h1').text

    assert title == 'OnlineMarket'
    assert content == 'We Serve For Customers And Small Businesses!'

@pytest.mark.acceptance
def test_marketplace_displayed(browser, base_url):
    marketplace_url = base_url + reverse('marketplace')
    browser.get(base_url)
    browser.find_element(By.LINK_TEXT, 'MARKET').click()
    current_url = browser.current_url

    browser.find_element(By.LINK_TEXT, 'CLOTHING SHOP').click()
    next_url = browser.current_url
    vendor_url = base_url + reverse('vendor_detail', args=['clothing-shop'])

    assert marketplace_url == current_url
    assert vendor_url == next_url

@pytest.mark.acceptance
def test_search(browser, base_url):
    browser.get(base_url)
    keyword = browser.find_element(By.NAME, 'keyword')
    keyword.send_keys('fruit')
    address = browser.find_element(By.NAME, 'address')
    address.send_keys('279 Amherst R')
    radius = browser.find_element(By.NAME, 'radius')
    radius.send_keys(15)

    search_url = base_url + reverse('search')
    browser.find_element(By.XPATH, "//input[@value='Search']").click()
    current_url = browser.current_url
    assert search_url in current_url

