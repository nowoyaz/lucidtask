"""
Модуль содержит маршруты API для регистрации и аутентификации пользователей.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.config import get_db
from app.services.user_service import create_user, authenticate_user, get_user_by_email
from app.middlewares.auth import create_simple_token
from app.schemas.user import UserCreate, UserLogin, TokenResponse

router = APIRouter(
    prefix="/api",
    tags=["authentication"]
)

@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Регистрация нового пользователя.
    
    Args:
        user_data (UserCreate): Данные для создания пользователя
        db (Session): Сессия базы данных
        
    Returns:
        TokenResponse: Ответ с токеном аутентификации
        
    Raises:
        HTTPException: Если пользователь с таким email уже существует
    """
    # Проверка, существует ли пользователь с таким email
    db_user = get_user_by_email(db, user_data.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже зарегистрирован"
        )
    
    # Создание пользователя
    user = create_user(db, user_data)
    
    # Аутентификация и получение ID пользователя
    user_id = authenticate_user(db, UserLogin(email=user_data.email, password=user_data.password))
    
    # Генерация токена
    token = create_simple_token(user_id)
    
    return {"token": token}

@router.post("/login", response_model=TokenResponse)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Вход пользователя в систему.
    
    Args:
        user_data (UserLogin): Данные для входа
        db (Session): Сессия базы данных
        
    Returns:
        TokenResponse: Ответ с токеном аутентификации
        
    Raises:
        HTTPException: Если аутентификация не удалась
    """
    # Аутентификация пользователя
    user_id = authenticate_user(db, user_data)
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль"
        )
    
    # Генерация токена
    token = create_simple_token(user_id)
    
    return {"token": token} 