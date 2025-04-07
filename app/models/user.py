"""
Модуль с определением модели пользователя для SQLAlchemy.
"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database.config import Base

class User(Base):
    """
    Модель пользователя для базы данных.
    
    Атрибуты:
        id (int): Уникальный идентификатор пользователя
        email (str): Email пользователя (уникальный)
        password (str): Хешированный пароль пользователя
        created_at (datetime): Дата и время создания пользователя
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False) 