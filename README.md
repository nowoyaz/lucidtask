# FastAPI User Posts Application

Веб-приложение на основе FastAPI с функционалом аутентификации и управления постами пользователей, следующее шаблону MVC.

## Структура проекта

```
app/
├── database/     # Конфигурация и подключение к БД
├── middlewares/  # Промежуточное ПО
├── models/       # Модели SQLAlchemy
├── routers/      # Маршрутизация API
├── schemas/      # Pydantic модели (схемы)
├── services/     # Бизнес-логика
└── main.py       # Точка входа приложения
```

## Установка

1. Клонируйте репозиторий
2. Создайте виртуальное окружение Python
3. Установите зависимости: `pip install -r requirements.txt`
4. База данных SQLite будет создана автоматически при первом запуске
5. Запустите приложение: `uvicorn app.main:app --reload`

## API Endpoints

- **POST /api/signup** - Регистрация нового пользователя
- **POST /api/login** - Вход в систему
- **POST /api/posts** - Добавление нового поста
- **GET /api/posts** - Получение всех постов пользователя
- **DELETE /api/posts/{post_id}** - Удаление поста 