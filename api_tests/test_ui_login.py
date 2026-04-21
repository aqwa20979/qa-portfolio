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
    """Тест 1: открыть сайт и проверить заголовок"""
    driver = get_driver()
    driver.get("https://www.saucedemo.com/")
    assert "Swag Labs" in driver.title
    driver.quit()

def test_login_valid():
    """Тест 2: авторизация"""
    driver = get_driver()
    driver.get("https://www.saucedemo.com/")
    username_field = driver.find_element(By.ID, "user-name")
    username_field.send_keys("standard_user")
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys("secret_sauce")
    login_button = driver.find_element(By.ID, "login-button")
    login_button.click()
    assert "inventory" in driver.current_url
    driver.quit()

def test_login_invalid():
    """Тест 3: негативный - неверный пароль"""
    driver = get_driver()
    driver.get("https://www.saucedemo.com/")
    username_field = driver.find_element(By.ID, "user-name")
    username_field.send_keys("standard_user")
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys("wrong_password")
    login_button = driver.find_element(By.ID, "login-button")
    login_button.click()
    error_message = driver.find_element(By.CSS_SELECTOR, "[data-test='error']")
    assert "Username and password do not match any user in this service" in error_message.text
    assert "inventory" not in driver.current_url
    driver.quit()

def test_add_to_cart():
    """Тест 4: добавление товара в корзину"""
    driver = get_driver()
    driver.get("https://www.saucedemo.com/")
    username_field = driver.find_element(By.ID, "user-name")
    username_field.send_keys("standard_user")
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys("secret_sauce")
    login_button = driver.find_element(By.ID, "login-button")
    login_button.click()
    add_button = driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack")
    add_button.click()
    cart_badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
    assert cart_badge.text == "1" 
    cart_icon = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
    cart_icon.click()
    cart_item = driver.find_element(By.CLASS_NAME, "inventory_item_name")
    assert cart_item.text == "Sauce Labs Backpack"
    driver.quit()

def test_checkout_order():
    """Тест 5: полное оформление заказа"""
    driver = get_driver()
    driver.get("https://www.saucedemo.com/")
    username_field = driver.find_element(By.ID, "user-name")
    username_field.send_keys("standard_user")
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys("secret_sauce")   
    login_button = driver.find_element(By.ID, "login-button")
    login_button.click()
    add_button = driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack")
    add_button.click()
    
    time.sleep(1)
    
    cart_icon = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
    cart_icon.click()
    
    time.sleep(1)
    
    checkout_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "checkout"))
    )
    checkout_button.click()
    
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "first-name"))
    )
    
    first_name_field = driver.find_element(By.ID, "first-name")
    first_name_field.send_keys("Иван")
    last_name_field = driver.find_element(By.ID, "last-name")
    last_name_field.send_keys("Тестов")
    postal_code_field = driver.find_element(By.ID, "postal-code")
    postal_code_field.send_keys("123456")
    continue_button = driver.find_element(By.ID, "continue")
    continue_button.click()
    finish_button = driver.find_element(By.ID, "finish")
    finish_button.click()
    
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))
    )
    
    success_message = driver.find_element(By.CLASS_NAME, "complete-header")
    assert "Thank you for your order" in success_message.text
    driver.quit()