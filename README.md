# QA Portfolio

## Обо мне

Здравствуйте! Меня зовут Роман.

QA Engineer с опытом написания автотестов на Python. Специализируюсь на API, UI и БД автоматизации. Умею строить тестовую инфраструктуру с нуля, генерировать отчёты и настраивать CI/CD.

## Технологический стек

- Python 3.14
- Pytest
- Requests (API тестирование)
- Playwright (UI тестирование)
- PostgreSQL + psycopg2 (БД тестирование)
- Postman + Newman (API коллекции)
- Allure (отчёты)
- Git / GitHub
- GitHub Actions (CI/CD)
- Docker

## Структура проекта

- qa_combined_project/
  - api_tests/
    - conftest.py
    - test_api_posts.py
    - test_schema.py
    - test_ui_playwright.py
    - test_database.py
  - postman/
    - JSONPlaceholder Tests.postman_collection.json
  - .github/workflows/
    - tests.yml
  - .gitignore
  - Dockerfile
  - requirements.txt
  - README.md

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

## Тестирование базы данных (8 штук) — PostgreSQL

Запущена БД в Docker-контейнере. Написаны автотесты на Python (pytest + psycopg2):

- Подключение к БД
- Создание таблиц (users, orders, products)
- Вставка тестовых данных
- Проверка SQL запросов: SELECT, JOIN, GROUP BY, HAVING, подзапросы, агрегатные функции

## Postman коллекция

В папке `postman` находится коллекция для тестирования API JSONPlaceholder.

### Что внутри

- GET запрос с проверками статуса и структуры ответа
- 6 автоматических тестов на JavaScript

### Импорт в Postman

1. Открой Postman
2. Нажми `Import` → `Upload Files`
3. Выбери файл `JSONPlaceholder Tests.postman_collection.json`

## Решение проблем: миграция с Selenium на Playwright

### Проблема
UI тесты на Selenium нестабильно работали в headless-режиме на GitHub Actions. Тест оформления заказа периодически падал с ошибкой NoSuchElementException.

### Анализ
- Локально все тесты проходили
- В CI тесты падали на разных шагах
- Проблема воспроизводилась только в headless-режиме

### Решение
Переписал UI тесты на Playwright:
- Встроенные умные ожидания
- Стабильная работа в headless-режиме
- Меньше кода при той же функциональности

### Результат
Все 5 UI тестов стабильно проходят в GitHub Actions.

## Docker

Тесты упакованы в Docker-контейнер для воспроизводимого запуска в любой среде.

### Сборка образа

docker build -t qa-portfolio .

### Запуск тестов

docker run --rm qa-portfolio

### Зависимости в контейнере

- Python 3.14
- Playwright + Chromium
- Pytest, Requests
- Системные библиотеки для headless-режима

## Allure отчёт

Онлайн отчёт доступен по ссылке:
https://aqwa20979.github.io/qa-portfolio/

## Запуск тестов

### Локально

Установка зависимостей:
pip install -r requirements.txt

API тесты:
pytest api_tests/test_api_posts.py -v

UI тесты:
pytest api_tests/test_ui_playwright.py -v

БД тесты:
pytest api_tests/test_database.py -v

Все тесты:
pytest api_tests/ -v

### Через Docker

docker build -t qa-portfolio .
docker run --rm qa-portfolio

## Контакты

- GitHub: github.com/aqwa20979
- Telegram: @romasha18
- Email: shamilov.roman@yandex.ru