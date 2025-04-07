"""
Модуль с определением модели поста для SQLAlchemy.
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.config import Base

class Post(Base):
    """
    Модель поста для базы данных.
    
    Атрибуты:
        id (int): Уникальный идентификатор поста
        text (str): Текст поста
        user_id (int): Идентификатор пользователя-автора
        created_at (datetime): Дата и время создания поста
        user (User): Отношение к модели пользователя
    """
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)

    # Связь с пользователем
    user = relationship("User", backref="posts") 