import psycopg2
import pytest

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        database="shop",
        user="postgres",
        password="mysecretpassword"
    )

def test_connection():
    """Тест 1: проверяем, что подключение к БД работает"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT 1")
    result = cur.fetchone()
    assert result[0] == 1
    cur.close()
    conn.close()

def test_create_tables():
    """Тест 2: создаём таблицы users, orders, products"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Создаём таблицу users
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            email VARCHAR(100),
            city VARCHAR(100)
        )
    """)
    
    # Создаём таблицу orders
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            total_amount DECIMAL(10,2),
            status VARCHAR(50)
        )
    """)
    
    # Создаём таблицу products
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            product_name VARCHAR(200),
            price DECIMAL(10,2)
        )
    """)
    
    conn.commit()
    
    # Проверяем, что таблицы создались
    cur.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
    """)
    tables = cur.fetchall()
    table_names = [t[0] for t in tables]
    
    assert 'users' in table_names
    assert 'orders' in table_names
    assert 'products' in table_names
    
    cur.close()
    conn.close()

def test_insert_data():
    """Тест 3: добавляем тестовые данные в таблицы"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Очищаем таблицы и сбрасываем счётчики id
    cur.execute("TRUNCATE TABLE orders RESTART IDENTITY CASCADE")
    cur.execute("TRUNCATE TABLE users RESTART IDENTITY CASCADE")
    cur.execute("TRUNCATE TABLE products RESTART IDENTITY CASCADE")
    
    # Вставляем пользователей
    cur.execute("""
        INSERT INTO users (name, email, city) VALUES
        ('Ivan Ivanov', 'ivan@mail.ru', 'Moscow'),
        ('Petr Petrov', 'petr@mail.ru', 'Saint Petersburg'),
        ('Sidor Sidorov', 'sidor@mail.ru', 'Moscow')
    """)
    
    # Вставляем товары
    cur.execute("""
        INSERT INTO products (product_name, price) VALUES
        ('Laptop', 50000.00),
        ('Mouse', 1500.00),
        ('Keyboard', 3000.00)
    """)
    
    # Вставляем заказы
    cur.execute("""
        INSERT INTO orders (user_id, total_amount, status) VALUES
        (1, 51500.00, 'completed'),
        (1, 1500.00, 'pending'),
        (2, 3000.00, 'completed')
    """)
    
    conn.commit()
    
    # Проверяем количество пользователей
    cur.execute("SELECT COUNT(*) FROM users")
    users_count = cur.fetchone()[0]
    assert users_count == 3
    
    # Проверяем количество товаров
    cur.execute("SELECT COUNT(*) FROM products")
    products_count = cur.fetchone()[0]
    assert products_count == 3
    
    cur.close()
    conn.close()

def test_select_with_join():
    """Тест 4: SELECT с JOIN — получить заказы с именами пользователей"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT o.id, u.name, o.total_amount, o.status
        FROM orders o
        JOIN users u ON o.user_id = u.id
    """)
    
    results = cur.fetchall()
    
    # Проверяем, что получили 3 заказа
    assert len(results) == 3
    
    # Проверяем, что у заказа есть имя пользователя
    for row in results:
        assert row[1] is not None
    
    cur.close()
    conn.close()

def test_group_by():
    """Тест 5: GROUP BY — количество заказов по пользователям"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT u.name, COUNT(o.id) as orders_count
        FROM users u
        LEFT JOIN orders o ON u.id = o.user_id
        GROUP BY u.id, u.name
        ORDER BY orders_count DESC
    """)
    
    results = cur.fetchall()
    
    # Проверяем, что у каждого пользователя есть количество заказов
    for row in results:
        assert row[1] is not None
    
    # Ivan Ivanov должен иметь 2 заказа
    for row in results:
        if row[0] == 'Ivan Ivanov':
            assert row[1] == 2
    
    # Petr Petrov должен иметь 1 заказ
    for row in results:
        if row[0] == 'Petr Petrov':
            assert row[1] == 1
    
    # Sidor Sidorov должен иметь 0 заказов
    for row in results:
        if row[0] == 'Sidor Sidorov':
            assert row[1] == 0
    
    cur.close()
    conn.close()

def test_group_by_with_having():
    """Тест 6: GROUP BY с HAVING — пользователи с суммой заказов больше 10000"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Добавляем большой заказ для проверки HAVING
    cur.execute("""
        INSERT INTO orders (user_id, total_amount, status) VALUES
        (1, 200000.00, 'completed')
    """)
    conn.commit()
    
    cur.execute("""
        SELECT u.name, SUM(o.total_amount) as total_spent
        FROM users u
        JOIN orders o ON u.id = o.user_id
        GROUP BY u.id, u.name
        HAVING SUM(o.total_amount) > 10000
        ORDER BY total_spent DESC
    """)
    
    results = cur.fetchall()
    
    # Должен быть хотя бы один пользователь с суммой > 10000
    assert len(results) >= 1
    
    # Ivan Ivanov должен быть в результате
    names = [row[0] for row in results]
    assert 'Ivan Ivanov' in names
    
    cur.close()
    conn.close()

def test_subquery():
    """Тест 7: подзапрос — найти пользователей, у которых есть заказы"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT name, email
        FROM users
        WHERE id IN (
            SELECT DISTINCT user_id
            FROM orders
        )
    """)
    
    results = cur.fetchall()
    
    # Пользователи с заказами: Ivan Ivanov и Petr Petrov
    assert len(results) == 2
    
    names = [row[0] for row in results]
    assert 'Ivan Ivanov' in names
    assert 'Petr Petrov' in names
    assert 'Sidor Sidorov' not in names
    
    cur.close()
    conn.close()

def test_aggregate_functions():
    """Тест 8: агрегатные функции — общая сумма всех заказов"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT 
            COUNT(*) as total_orders,
            SUM(total_amount) as total_revenue,
            AVG(total_amount) as avg_order,
            MIN(total_amount) as min_order,
            MAX(total_amount) as max_order
        FROM orders
    """)
    
    result = cur.fetchone()
    
    total_orders, total_revenue, avg_order, min_order, max_order = result
    
    # Всего должно быть 4 заказа (3 из предыдущих + 1 большой)
    assert total_orders == 4
    
    # Минимальный заказ = 1500
    assert min_order == 1500
    
    # Максимальный заказ = 200000
    assert max_order == 200000
    
    cur.close()
    conn.close()