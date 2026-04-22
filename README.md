# QA Portfolio

## Обо мне

Здравствуйте! Меня зовут Роман.

QA Engineer с опытом написания автотестов на Python. Специализируюсь на API и UI автоматизации. Умею строить тестовую инфраструктуру с нуля, генерировать отчёты и настраивать CI/CD.

## Технологический стек

- Python 3.14
- Pytest
- Requests (API тестирование)
- Selenium (UI тестирование)
- Playwright (UI тестирование)
- Allure (отчёты)
- Git / GitHub
- GitHub Pages
- GitHub Actions (CI/CD)

## Структура проекта
qa_combined_project/
├── api_tests/
│ ├── conftest.py
│ ├── test_api_posts.py
│ ├── test_schema.py
│ └── test_ui_playwright.py
├── .github/
│ └── workflows/
│ └── tests.yml
├── .gitignore
└── README.md

text

## API тесты (6 штук)

JSONPlaceholder

- GET /posts/1 - получение поста, статус 200
- GET /posts/999 - негативный сценарий, статус 404
- POST /posts - создание поста, статус 201
- DELETE /posts/1 - удаление поста, статус 200
- DELETE /posts/999 - удаление несуществующего поста (особенность API)
- Проверка схемы ответа - валидация полей и типов данных

## UI тесты (5 штук) — Playwright

SauceDemo (все тесты стабильно проходят в CI)

- Открытие сайта
- Успешная авторизация
- Неверный пароль
- Добавление в корзину
- Оформление заказа

Все 11 тестов проходят стабильно.

## Решение проблем: миграция с Selenium на Playwright

### Проблема
UI тесты на Selenium нестабильно работали в headless-режиме на GitHub Actions. Тест оформления заказа периодически падал с ошибкой `NoSuchElementException` — браузер не успевал загрузить страницу корзины или форму оформления, несмотря на явные ожидания.

### Анализ
- Локально все тесты проходили
- В CI тесты падали на разных шагах (кнопка checkout, поле first-name, кнопка finish)
- Проблема воспроизводилась только в headless-режиме
- Selenium + ChromeDriver в CI показали себя нестабильно

### Решение
Переписал UI тесты на Playwright:
- Встроенные умные ожидания (не нужны явные WebDriverWait)
- Стабильная работа в headless-режиме
- Меньше кода при той же функциональности

### Результат
Все 5 UI тестов стабильно проходят в GitHub Actions.

## Allure отчёт

Онлайн отчёт доступен по ссылке:
https://aqwa20979.github.io/qa-portfolio/

## Запуск тестов

Установка зависимостей:
pip install -r requirements.txt

API тесты:
pytest api_tests/test_api_posts.py -v

UI тесты:
pytest api_tests/test_ui_playwright.py -v

Все тесты:
pytest api_tests/ -v

## Контакты

- GitHub: github.com/aqwa20979
- Telegram: @romasha18
- Email: shamilov.roman@yandex.ru
