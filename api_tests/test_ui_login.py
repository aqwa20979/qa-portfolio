import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

def test_open_saucedemo():
    """Тест 1: открыть сайт и проверить заголовок"""
    driver = webdriver.Chrome()
    driver.get("https://www.saucedemo.com/")
    assert "Swag Labs" in driver.title
    driver.quit()

def test_login_valid():
    """Тест 2: авторизация"""
    driver = webdriver.Chrome()
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
    """Тест 3: негатвиный - неверный пароль"""
    driver = webdriver.Chrome()
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
    driver = webdriver.Chrome()
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
    cart_item = driver.find_element(By.CLASS_NAME, "inventory_item_name" )
    assert cart_item.text == "Sauce Labs Backpack"
    driver.quit()

def test_checkout_order():
    """Тест 5: полное оформление заказа"""
    driver = webdriver.Chrome()
    driver.get("https://www.saucedemo.com/")
    username_field = driver.find_element(By.ID, "user-name")
    username_field.send_keys("standard_user")
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys("secret_sauce")   
    login_button = driver.find_element(By.ID, "login-button")
    login_button.click()
    add_button = driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack")
    add_button.click()
    cart_icon = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
    cart_icon.click()
    checkout_button = driver.find_element(By.ID, "checkout")
    checkout_button.click()
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
    success_message = driver.find_element(By.CLASS_NAME, "complete-header")
    assert "Thank you for your order" in success_message.text
    driver.quit()