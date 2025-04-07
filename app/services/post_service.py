"""
Модуль содержит бизнес-логику для работы с постами.
"""
from sqlalchemy.orm import Session
from app.models.post import Post
from app.models.user import User
from app.schemas.post import PostCreate, PostResponse
from typing import List, Optional
from fastapi import HTTPException, status

def create_post(db: Session, post: PostCreate, user_id: int) -> Post:
    """
    Создает новый пост.
    
    Args:
        db (Session): Сессия базы данных
        post (PostCreate): Данные поста
        user_id (int): ID пользователя-автора
        
    Returns:
        Post: Созданный пост
    """
    # Создание поста
    db_post = Post(text=post.text, user_id=user_id)
    
    # Сохранение поста в БД
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    
    return db_post

def get_user_posts(db: Session, user_id: int) -> List[Post]:
    """
    Получает все посты пользователя.
    
    Args:
        db (Session): Сессия базы данных
        user_id (int): ID пользователя
        
    Returns:
        List[Post]: Список постов пользователя
    """
    return db.query(Post).filter(Post.user_id == user_id).all()

def get_post_by_id(db: Session, post_id: int) -> Optional[Post]:
    """
    Получает пост по ID.
    
    Args:
        db (Session): Сессия базы данных
        post_id (int): ID поста
        
    Returns:
        Optional[Post]: Найденный пост или None
    """
    return db.query(Post).filter(Post.id == post_id).first()

def delete_post(db: Session, post_id: int, user_id: int) -> bool:
    """
    Удаляет пост.
    
    Args:
        db (Session): Сессия базы данных
        post_id (int): ID поста
        user_id (int): ID пользователя-владельца
        
    Returns:
        bool: True, если пост успешно удален, иначе False
        
    Raises:
        HTTPException: Если пост не найден или пользователь не является владельцем
    """
    # Получение поста
    post = get_post_by_id(db, post_id)
    
    # Проверка наличия поста
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пост с ID {post_id} не найден"
        )
    
    # Проверка владельца поста
    if post.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет прав для удаления этого поста"
        )
    
    # Удаление поста
    db.delete(post)
    db.commit()
    
    return True 