"""
Модуль содержит Pydantic-модели для валидации данных постов.
"""
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    """
    Базовая схема поста.
    
    Атрибуты:
        text (str): Текст поста
    """
    text: str = Field(..., min_length=1, max_length=1000000, description="Текст поста")
    
    @validator('text')
    def validate_text_size(cls, v):
        """
        Валидатор для проверки размера текста поста.
        
        Args:
            v (str): Текст поста
            
        Returns:
            str: Проверенный текст
            
        Raises:
            ValueError: Если размер текста превышает 1 МБ
        """
        # Проверка на размер (примерно 1 МБ)
        if len(v.encode('utf-8')) > 1_000_000:
            raise ValueError('Размер поста не должен превышать 1 МБ')
        return v

class PostCreate(PostBase):
    """
    Схема для создания поста.
    
    Атрибуты:
        text (str): Текст поста
    """
    pass

class PostResponse(PostBase):
    """
    Схема для ответа с данными поста.
    
    Атрибуты:
        id (int): Идентификатор поста
        text (str): Текст поста
        created_at (datetime): Дата и время создания поста
        user_id (int): Идентификатор пользователя-автора
    """
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        orm_mode = True
        
class PostDelete(BaseModel):
    """
    Схема для удаления поста.
    
    Атрибуты:
        post_id (int): Идентификатор поста для удаления
    """
    post_id: int = Field(..., description="Идентификатор поста для удаления") 