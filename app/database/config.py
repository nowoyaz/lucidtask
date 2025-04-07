"""
Модуль конфигурации базы данных.
Содержит настройки подключения к SQLite и создание сессии SQLAlchemy.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Создание директории для базы данных, если она не существует
os.makedirs("./data", exist_ok=True)

# Строка подключения к базе данных (SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///./data/app.db"

# Создание движка SQLAlchemy с поддержкой внешних ключей для SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Создание класса SessionLocal для создания экземпляров сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей SQLAlchemy
Base = declarative_base()

# Функция зависимостей для получения сессии БД
def get_db():
    """
    Функция-зависимость для получения сессии базы данных.
    
    Yields:
        Session: Объект сессии базы данных.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 