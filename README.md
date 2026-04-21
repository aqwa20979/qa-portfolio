# QA Portfolio

## Обо мне
Здравствуйте! Меня зовут Роман.
QA Engineer с опытом написания автотестов на Python. Специализируюсь на API и UI автоматизации. Умею строить тестовую инфраструктуру с нуля, генерировать отчёты и настраивать CI/CD.

## Технологический стек

- Python 3.14
- Pytest
- Requests (API тестирование)
- Selenium (UI тестирование)
- Allure (отчёты)
- Git / GitHub
- GitHub Pages

## Структура проекта

qa_combined_project/
├── api_tests/
│   ├── conftest.py
│   ├── test_api_posts.py
│   ├── test_schema.py
│   └── test_ui_login.py
├── .gitignore
└── README.md

## API тесты (6 штук)

JSONPlaceholder

- GET /posts/1 - получение поста, статус 200
- GET /posts/999 - негативный сценарий, статус 404
- POST /posts - создание поста, статус 201
- DELETE /posts/1 - удаление поста, статус 200
- DELETE /posts/999 - удаление несуществующего поста (особенность API)
- Проверка схемы ответа - валидация полей и типов данных

## UI тесты (5 штук)

SauceDemo

- Открытие сайта - проверка заголовка
- Успешная авторизация - переход на страницу товаров
- Неверный пароль - сообщение об ошибке
- Добавление в корзину - проверка счётчика
- Оформление заказа - полный E2E сценарий

Все 11 тестов проходят стабильно.

## Allure отчёт

Онлайн отчёт доступен по ссылке:
https://aqwa20979.github.io/qa-portfolio/

## Запуск тестов

Установка зависимостей:
pip install -r requirements.txt

API тесты:
pytest api_tests/test_api_posts.py -v

UI тесты:
pytest api_tests/test_ui_login.py -v

Все тесты:
pytest api_tests/ -v

## Контакты

GitHub: github.com/aqwa20979
Telegram: @romasha18
Email: shamilov.roman@yandex.ru

Портфолио обновляется. Новые тесты и проекты в разработке.