"""
Модуль содержит бизнес-логику для работы с пользователями.
"""
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from passlib.context import CryptContext
from typing import Optional

# Создание контекста для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """
    Создает хеш пароля.
    
    Args:
        password (str): Пароль в открытом виде
        
    Returns:
        str: Хешированный пароль
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет соответствие пароля его хешу.
    
    Args:
        plain_password (str): Пароль в открытом виде
        hashed_password (str): Хешированный пароль
        
    Returns:
        bool: True, если пароль соответствует хешу, иначе False
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Получает пользователя по email.
    
    Args:
        db (Session): Сессия базы данных
        email (str): Email пользователя
        
    Returns:
        Optional[User]: Найденный пользователь или None
    """
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """
    Получает пользователя по ID.
    
    Args:
        db (Session): Сессия базы данных
        user_id (int): ID пользователя
        
    Returns:
        Optional[User]: Найденный пользователь или None
    """
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user: UserCreate) -> User:
    """
    Создает нового пользователя.
    
    Args:
        db (Session): Сессия базы данных
        user (UserCreate): Данные пользователя
        
    Returns:
        User: Созданный пользователь
    """
    # Хеширование пароля
    hashed_password = get_password_hash(user.password)
    
    # Создание пользователя
    db_user = User(email=user.email, password=hashed_password)
    
    # Сохранение пользователя в БД
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

def authenticate_user(db: Session, user_data: UserLogin) -> Optional[int]:
    """
    Аутентифицирует пользователя.
    
    Args:
        db (Session): Сессия базы данных
        user_data (UserLogin): Данные для входа
        
    Returns:
        Optional[int]: ID пользователя, если аутентификация успешна, иначе None
    """
    # Поиск пользователя в БД
    user = get_user_by_email(db, user_data.email)
    
    # Проверка наличия пользователя и пароля
    if not user or not verify_password(user_data.password, user.password):
        return None
    
    # Возвращаем ID пользователя
    return user.id 