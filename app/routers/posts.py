"""
Модуль содержит маршруты API для работы с постами пользователей.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from typing import List
from app.database.config import get_db
from app.middlewares.auth import get_current_user_id
from app.middlewares.caching import cache_response, invalidate_cache
from app.services.post_service import create_post, get_user_posts, delete_post
from app.services.user_service import get_user_by_id
from app.models.user import User
from app.schemas.post import PostCreate, PostResponse, PostDelete

router = APIRouter(
    prefix="/api/posts",
    tags=["posts"]
)

@router.post("", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def add_post(
    post_data: PostCreate,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Создание нового поста.
    
    Args:
        post_data (PostCreate): Данные для создания поста
        user_id (int): ID текущего аутентифицированного пользователя
        db (Session): Сессия базы данных
        
    Returns:
        PostResponse: Созданный пост
    """
    # Проверка наличия пользователя
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден"
        )
    
    # Создание поста
    post = create_post(db, post_data, user_id)
    
    # Инвалидируем кеш для запроса постов этого пользователя
    invalidate_cache(user_id, "get_posts")
    
    return post

@router.get("", response_model=List[PostResponse])
@cache_response("get_posts")
async def get_posts(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Получение всех постов пользователя.
    
    Args:
        user_id (int): ID текущего аутентифицированного пользователя
        db (Session): Сессия базы данных
        
    Returns:
        List[PostResponse]: Список постов пользователя
    """
    # Проверка наличия пользователя
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден"
        )
    
    # Получение постов
    posts = get_user_posts(db, user_id)
    
    return posts

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_post(
    post_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Удаление поста.
    
    Args:
        post_id (int): ID поста для удаления
        user_id (int): ID текущего аутентифицированного пользователя
        db (Session): Сессия базы данных
        
    Returns:
        None
    """
    # Проверка наличия пользователя
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Пользователь не найден"
        )
    
    # Удаление поста
    delete_post(db, post_id, user_id)
    
    # Инвалидируем кеш для запроса постов этого пользователя
    invalidate_cache(user_id, "get_posts")
    
    # Возвращаем 204 No Content
    return None 