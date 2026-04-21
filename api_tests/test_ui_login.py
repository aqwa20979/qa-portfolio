import pytest
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
    options.add_argument('--window-size=1920,1080')
    return webdriver.Chrome(options=options)


@pytest.fixture
def driver():
    driver = get_driver()
    yield driver
    driver.quit()


def test_open_saucedemo(driver):
    driver.get("https://www.saucedemo.com/")
    WebDriverWait(driver, 10).until(EC.title_contains("Swag Labs"))
    assert "Swag Labs" in driver.title


def test_login_valid(driver):
    driver.get("https://www.saucedemo.com/")

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "user-name"))
    ).send_keys("standard_user")

    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    WebDriverWait(driver, 10).until(
        EC.url_contains("inventory")
    )
    assert "inventory" in driver.current_url


def test_login_invalid(driver):
    driver.get("https://www.saucedemo.com/")

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "user-name"))
    ).send_keys("standard_user")

    driver.find_element(By.ID, "password").send_keys("wrong_password")
    driver.find_element(By.ID, "login-button").click()

    error = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
    )

    assert "do not match" in error.text
    assert "inventory" not in driver.current_url


def test_add_to_cart(driver):
    driver.get("https://www.saucedemo.com/")

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "user-name"))
    ).send_keys("standard_user")

    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))
    ).click()

    badge = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge"))
    )

    assert badge.text == "1"


def test_checkout_order(driver):
    driver.get("https://www.saucedemo.com/")

    # Логин
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "user-name"))
    ).send_keys("standard_user")

    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    # Добавление товара
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))
    ).click()

    # Переход в корзину
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link"))
    ).click()

    # Checkout
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "checkout"))
    ).click()

    # Заполнение формы
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "first-name"))
    )

    driver.find_element(By.ID, "first-name").send_keys("Ivan")
    driver.find_element(By.ID, "last-name").send_keys("Test")
    driver.find_element(By.ID, "postal-code").send_keys("123456")
    driver.find_element(By.ID, "continue").click()

    # 🔥 КЛЮЧЕВОЙ ФИКС — ждём переход на overview
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "summary_info"))
    )

    # Finish
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "finish"))
    ).click()

    # Проверка успешного заказа
    success_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "complete-header"))
    )

    assert "Thank you for your order" in success_message.text