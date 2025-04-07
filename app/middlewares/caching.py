"""
Модуль содержит функции и классы для кэширования ответов API.
"""
from fastapi import Request, Response
from typing import Dict, Any, Callable
import time
from functools import wraps

# Простой кэш в памяти
# Ключ: user_id-endpoint, значение: (timestamp, cached_data)
cache_storage: Dict[str, tuple] = {}

# Время жизни кэша в секундах (5 минут)
CACHE_TTL = 300

def get_cache_key(user_id: int, endpoint: str) -> str:
    """
    Генерирует ключ кэша на основе ID пользователя и эндпоинта.
    
    Args:
        user_id (int): ID пользователя
        endpoint (str): Эндпоинт API
        
    Returns:
        str: Ключ кэша
    """
    return f"{user_id}-{endpoint}"

def get_cached_data(user_id: int, endpoint: str) -> Any:
    """
    Получает данные из кэша, если они не устарели.
    
    Args:
        user_id (int): ID пользователя
        endpoint (str): Эндпоинт API
        
    Returns:
        Any: Кэшированные данные или None, если данных нет или они устарели
    """
    key = get_cache_key(user_id, endpoint)
    
    if key in cache_storage:
        timestamp, data = cache_storage[key]
        current_time = time.time()
        
        # Проверяем, не устарел ли кэш
        if current_time - timestamp <= CACHE_TTL:
            return data
    
    return None

def set_cache_data(user_id: int, endpoint: str, data: Any) -> None:
    """
    Сохраняет данные в кэш.
    
    Args:
        user_id (int): ID пользователя
        endpoint (str): Эндпоинт API
        data (Any): Данные для кэширования
    """
    key = get_cache_key(user_id, endpoint)
    current_time = time.time()
    cache_storage[key] = (current_time, data)

def invalidate_cache(user_id: int, endpoint: str) -> None:
    """
    Инвалидирует (удаляет) кеш для указанного пользователя и эндпоинта.
    
    Args:
        user_id (int): ID пользователя
        endpoint (str): Эндпоинт API
    """
    key = get_cache_key(user_id, endpoint)
    if key in cache_storage:
        del cache_storage[key]

def cache_response(endpoint: str):
    """
    Декоратор для кэширования ответов API.
    
    Args:
        endpoint (str): Название эндпоинта для формирования ключа кэша
        
    Returns:
        Callable: Декорированная функция
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Получаем user_id из аргументов
            user_id = kwargs.get('user_id')
            if not user_id:
                # Если user_id не найден в kwargs, ищем в args
                for arg in args:
                    if isinstance(arg, int):
                        user_id = arg
                        break
            
            if not user_id:
                # Если user_id не найден, не используем кэш
                return await func(*args, **kwargs)
            
            # Проверяем кэш
            cached_data = get_cached_data(user_id, endpoint)
            if cached_data is not None:
                return cached_data
            
            # Выполняем оригинальную функцию
            result = await func(*args, **kwargs)
            
            # Сохраняем результат в кэш
            set_cache_data(user_id, endpoint, result)
            
            return result
        return wrapper
    return decorator 