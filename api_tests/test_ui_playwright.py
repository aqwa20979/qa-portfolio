import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture
def browser_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        yield page
        browser.close()

def test_open_saucedemo(browser_page):
    """Тест 1: открыть сайт и проверить заголовок"""
    browser_page.goto("https://www.saucedemo.com/")
    assert "Swag Labs" in browser_page.title()

def test_login_valid(browser_page):
    """Тест 2: авторизация с правильным паролем"""
    browser_page.goto("https://www.saucedemo.com/")
    browser_page.fill("#user-name", "standard_user")
    browser_page.fill("#password", "secret_sauce")
    browser_page.click("#login-button")
    assert "inventory" in browser_page.url

def test_login_invalid(browser_page):
    """Тест 3: негативный - неверный пароль"""
    browser_page.goto("https://www.saucedemo.com/")
    browser_page.fill("#user-name", "standard_user")
    browser_page.fill("#password", "wrong_password")
    browser_page.click("#login-button")
    error = browser_page.locator("[data-test='error']")
    assert "do not match" in error.text_content()
    assert "inventory" not in browser_page.url

def test_add_to_cart(browser_page):
    """Тест 4: добавление товара в корзину"""
    browser_page.goto("https://www.saucedemo.com/")
    browser_page.fill("#user-name", "standard_user")
    browser_page.fill("#password", "secret_sauce")
    browser_page.click("#login-button")
    browser_page.click("#add-to-cart-sauce-labs-backpack")
    badge = browser_page.locator(".shopping_cart_badge")
    assert badge.text_content() == "1"

def test_checkout_order(browser_page):
    """Тест 5: полное оформление заказа (Playwright - стабильно)"""
    browser_page.goto("https://www.saucedemo.com/")
    browser_page.fill("#user-name", "standard_user")
    browser_page.fill("#password", "secret_sauce")
    browser_page.click("#login-button")
    browser_page.click("#add-to-cart-sauce-labs-backpack")
    browser_page.click(".shopping_cart_link")
    browser_page.click("#checkout")
    browser_page.fill("#first-name", "Ivan")
    browser_page.fill("#last-name", "Test")
    browser_page.fill("#postal-code", "123456")
    browser_page.click("#continue")
    browser_page.click("#finish")
    success = browser_page.locator(".complete-header")
    assert "Thank you for your order" in success.text_content()