"""
Модуль содержит middleware и функции для работы с аутентификацией.
"""
import jwt
from fastapi import Depends, HTTPException, Header, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta
from app.database.config import get_db
import secrets
import string

# Настройки для JWT токена
SECRET_KEY = "YOUR_SECRET_KEY_HERE"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Для имитации хранения простых токенов доступа (для более простой реализации)
# В реальном приложении следует использовать базу данных или Redis
token_storage = {}

security = HTTPBearer()

def create_jwt_token(user_id: int) -> str:
    """
    Создает JWT токен для пользователя.
    
    Args:
        user_id (int): Идентификатор пользователя
        
    Returns:
        str: Сгенерированный JWT токен
    """
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + expires_delta
    
    to_encode = {"sub": str(user_id), "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_simple_token(user_id: int) -> str:
    """
    Создает простой токен для пользователя.
    
    Args:
        user_id (int): Идентификатор пользователя
        
    Returns:
        str: Сгенерированный токен
    """
    # Генерация случайного токена
    alphabet = string.ascii_letters + string.digits
    token = ''.join(secrets.choice(alphabet) for _ in range(32))
    
    # Сохранение связи токена с пользователем
    token_storage[token] = user_id
    
    return token

def verify_token(token: str) -> Optional[int]:
    """
    Проверяет валидность токена.
    
    Args:
        token (str): Токен для проверки
        
    Returns:
        Optional[int]: Идентификатор пользователя, если токен валиден, иначе None
    """
    # Проверка по хранилищу токенов
    if token in token_storage:
        return token_storage[token]
    
    # Попытка расшифровать JWT токен
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        return user_id
    except (Exception, ValueError):
        return None

def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> int:
    """
    Получает ID текущего пользователя на основе токена.
    
    Args:
        credentials (HTTPAuthorizationCredentials): Учетные данные авторизации
        
    Returns:
        int: ID пользователя
        
    Raises:
        HTTPException: Если токен недействителен
    """
    token = credentials.credentials
    user_id = verify_token(token)
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный токен аутентификации",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user_id 