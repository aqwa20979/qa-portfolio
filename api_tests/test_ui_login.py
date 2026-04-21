import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException


# ---------- DRIVER ----------

def get_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    return webdriver.Chrome(options=options)


@pytest.fixture
def driver():
    driver = get_driver()
    yield driver
    driver.quit()


# ---------- HELPERS ----------

def wait_and_click(driver, locator, timeout=15):
    return WebDriverWait(driver, timeout, ignored_exceptions=(StaleElementReferenceException,)).until(
        EC.element_to_be_clickable(locator)
    ).click()


def wait_visible(driver, locator, timeout=15):
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located(locator)
    )


def wait_url_contains(driver, text, timeout=15):
    WebDriverWait(driver, timeout).until(
        EC.url_contains(text)
    )


# ---------- TESTS ----------

def test_open_saucedemo(driver):
    driver.get("https://www.saucedemo.com/")
    WebDriverWait(driver, 10).until(EC.title_contains("Swag Labs"))
    assert "Swag Labs" in driver.title


def test_login_valid(driver):
    driver.get("https://www.saucedemo.com/")

    wait_visible(driver, (By.ID, "user-name")).send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")

    wait_and_click(driver, (By.ID, "login-button"))

    wait_url_contains(driver, "inventory")
    assert "inventory" in driver.current_url


def test_login_invalid(driver):
    driver.get("https://www.saucedemo.com/")

    wait_visible(driver, (By.ID, "user-name")).send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("wrong_password")

    wait_and_click(driver, (By.ID, "login-button"))

    error = wait_visible(driver, (By.CSS_SELECTOR, "[data-test='error']"))

    assert "do not match" in error.text
    assert "inventory" not in driver.current_url


def test_add_to_cart(driver):
    driver.get("https://www.saucedemo.com/")

    wait_visible(driver, (By.ID, "user-name")).send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")

    wait_and_click(driver, (By.ID, "login-button"))
    wait_url_contains(driver, "inventory")

    wait_and_click(driver, (By.ID, "add-to-cart-sauce-labs-backpack"))

    badge = wait_visible(driver, (By.CLASS_NAME, "shopping_cart_badge"))
    assert badge.text == "1"


def test_checkout_order(driver):
    driver.get("https://www.saucedemo.com/")

    # --- LOGIN ---
    wait_visible(driver, (By.ID, "user-name")).send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    wait_and_click(driver, (By.ID, "login-button"))

    wait_url_contains(driver, "inventory")

    # --- ADD TO CART ---
    wait_and_click(driver, (By.ID, "add-to-cart-sauce-labs-backpack"))

    # --- OPEN CART ---
    wait_and_click(driver, (By.CLASS_NAME, "shopping_cart_link"))

    # 🔥 Ждём именно страницу корзины
    wait_url_contains(driver, "cart")
    wait_visible(driver, (By.CLASS_NAME, "cart_item"))

    # --- CHECKOUT ---
    wait_and_click(driver, (By.ID, "checkout"))

    # 🔥 Ждём checkout step one
    wait_url_contains(driver, "checkout-step-one")

    # --- FORM ---
    wait_visible(driver, (By.ID, "first-name")).send_keys("Ivan")
    driver.find_element(By.ID, "last-name").send_keys("Test")
    driver.find_element(By.ID, "postal-code").send_keys("123456")

    wait_and_click(driver, (By.ID, "continue"))

    # 🔥 Ждём overview page
    wait_url_contains(driver, "checkout-step-two")
    wait_visible(driver, (By.CLASS_NAME, "summary_info"))

    # --- FINISH ---
    wait_and_click(driver, (By.ID, "finish"))

    # 🔥 Ждём success page
    wait_url_contains(driver, "checkout-complete")

    success = wait_visible(driver, (By.CLASS_NAME, "complete-header"))
    assert "Thank you for your order" in success.text


# ---------- DEBUG (скрин при падении) ----------

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if driver:
            driver.save_screenshot(f"screenshot_{item.name}.png")