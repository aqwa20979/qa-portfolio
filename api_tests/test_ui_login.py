import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--remote-debugging-port=9222')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-blink-features=AutomationControlled')
    return webdriver.Chrome(options=options)

def test_open_saucedemo():
    driver = get_driver()
    driver.get("https://www.saucedemo.com/")
    assert "Swag Labs" in driver.title
    driver.quit()

def test_login_valid():
    driver = get_driver()
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    assert "inventory" in driver.current_url
    driver.quit()

def test_login_invalid():
    driver = get_driver()
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("wrong_password")
    driver.find_element(By.ID, "login-button").click()
    error = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
    assert "do not match" in error.text
    assert "inventory" not in driver.current_url
    driver.quit()

def test_add_to_cart():
    driver = get_driver()
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
    assert badge.text == "1"
    driver.quit()

# def test_checkout_step_by_step():
#     driver = get_driver()
#     driver.get("https://www.saucedemo.com/")
#     WebDriverWait(driver, 20).until(
#         EC.presence_of_element_located((By.ID, "user-name"))
#     ).send_keys("standard_user")
#     driver.find_element(By.ID, "password").send_keys("secret_sauce")
#     driver.find_element(By.ID, "login-button").click()
#     WebDriverWait(driver, 20).until(
#         EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))
#     ).click()
#     driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
#     time.sleep(3)
#     cart_item = driver.find_element(By.CLASS_NAME, "inventory_item_name")
#     assert cart_item.text == "Sauce Labs Backpack"
#     checkout = driver.find_element(By.ID, "checkout")
#     checkout.click()
#     WebDriverWait(driver, 20).until(
#         EC.presence_of_element_located((By.ID, "first-name"))
#     ).send_keys("Ivan")
#     driver.find_element(By.ID, "last-name").send_keys("Test")
#     driver.find_element(By.ID, "postal-code").send_keys("123456")
#     driver.find_element(By.ID, "continue").click()
#     WebDriverWait(driver, 20).until(
#         EC.element_to_be_clickable((By.ID, "finish"))
#     ).click()
#     success = WebDriverWait(driver, 20).until(
#         EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))
#     )
#     assert "Thank you for your order" in success.text
#     driver.quit()