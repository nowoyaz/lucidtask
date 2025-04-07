"""
Модуль содержит Pydantic-модели для валидации данных пользователя.
"""
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
import re

class UserBase(BaseModel):
    """
    Базовая схема пользователя.
    
    Атрибуты:
        email (EmailStr): Email пользователя
    """
    email: EmailStr = Field(..., description="Email пользователя")

class UserCreate(UserBase):
    """
    Схема для создания пользователя.
    
    Атрибуты:
        email (EmailStr): Email пользователя
        password (str): Пароль пользователя
    """
    password: str = Field(..., min_length=6, max_length=100, description="Пароль пользователя")
    
    @validator('password')
    def password_must_be_strong(cls, v):
        """
        Валидатор для проверки сложности пароля.
        
        Args:
            v (str): Проверяемый пароль
            
        Returns:
            str: Проверенный пароль
            
        Raises:
            ValueError: Если пароль не соответствует требованиям
        """
        if not re.search(r'[A-Z]', v):
            raise ValueError('Пароль должен содержать хотя бы одну заглавную букву')
        if not re.search(r'[a-z]', v):
            raise ValueError('Пароль должен содержать хотя бы одну строчную букву')
        if not re.search(r'[0-9]', v):
            raise ValueError('Пароль должен содержать хотя бы одну цифру')
        return v

class UserLogin(BaseModel):
    """
    Схема для входа пользователя.
    
    Атрибуты:
        email (EmailStr): Email пользователя
        password (str): Пароль пользователя
    """
    email: EmailStr = Field(..., description="Email пользователя")
    password: str = Field(..., min_length=6, max_length=100, description="Пароль пользователя")

class UserOut(UserBase):
    """
    Схема для вывода информации о пользователе.
    
    Атрибуты:
        id (int): Идентификатор пользователя
        email (EmailStr): Email пользователя
        created_at (datetime): Дата и время создания пользователя
    """
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True
        
class TokenResponse(BaseModel):
    """
    Схема для ответа с токеном.
    
    Атрибуты:
        token (str): Токен авторизации
    """
    token: str = Field(..., description="Токен авторизации") 