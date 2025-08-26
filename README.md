# Task Manager API

Task Manager API — это асинхронный REST API сервис для управления задачами. Проект реализован на FastAPI с
использованием SQLAlchemy и SQLite.

## Основные возможности

- Создание задач
- Получение списка задач с пагинацией
- Получение задачи по идентификатору
- Обновление задачи
- Удаление задачи
- Health-check для проверки доступности сервиса
- Тесты на эндпоинты

## Стек технологий

- Python 3.12
- FastAPI
- SQLAlchemy (Async ORM)
- Pytest (тестирование)

## Установка и запуск

1. Клонирование репозитория

```bash
git clone https://github.com/xknowen/task_manager.git
cd task_manager
```

2. Создание виртуального окружения и установка зависимостей

python -m venv .venv

source .venv/bin/activate # Linux/Mac

.venv\Scripts\activate # Windows

pip install -r requirements.txt

3. Настройка переменных окружения

Создайте файл .env в корне проекта и укажите настройки в соответствии с .env.template

