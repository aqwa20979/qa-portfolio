def test_checkout_step_by_step():
    """Тест 5a: пошаговая проверка оформления"""
    driver = get_driver()
    driver.get("https://www.saucedemo.com/")
    
    # Шаг 1: логин
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "user-name"))
    ).send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    
    # Шаг 2: добавить товар
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))
    ).click()
    
    # Шаг 3: открыть корзину
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    
    # Шаг 4: проверить, что товар в корзине
    cart_item = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "inventory_item_name"))
    )
    assert cart_item.text == "Sauce Labs Backpack"
    
    # Шаг 5: нажать Checkout
    driver.find_element(By.ID, "checkout").click()
    
    # Шаг 6: заполнить форму
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "first-name"))
    ).send_keys("Ivan")
    driver.find_element(By.ID, "last-name").send_keys("Test")
    driver.find_element(By.ID, "postal-code").send_keys("123456")
    driver.find_element(By.ID, "continue").click()
    
    # Шаг 7: проверить, что на странице подтверждения
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "summary_total_label"))
    )
    
    # Шаг 8: нажать Finish
    driver.find_element(By.ID, "finish").click()
    
    # Шаг 9: проверить успех
    success = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "complete-header"))
    )
    assert "Thank you for your order" in success.text
    
    driver.quit()