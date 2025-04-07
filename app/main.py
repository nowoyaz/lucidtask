"""
Главный модуль приложения FastAPI.
"""
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError

from app.database.config import engine, Base
from app.routers import auth, posts

# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)

# Инициализация приложения FastAPI
app = FastAPI(
    title="User Posts API",
    description="API для управления постами пользователей",
    version="1.0.0"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(auth.router)
app.include_router(posts.router)

@app.get("/")
async def root():
    """
    Корневой endpoint API.
    
    Returns:
        dict: Информация о приложении
    """
    return {
        "message": "Добро пожаловать в API управления постами пользователей",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.middleware("http")
async def db_exception_handler(request: Request, call_next):
    """
    Middleware для обработки исключений SQLAlchemy.
    
    Args:
        request (Request): Объект запроса FastAPI
        call_next: Следующий обработчик в цепочке
        
    Returns:
        Response: Объект ответа
    """
    try:
        return await call_next(request)
    except SQLAlchemyError as exc:
        # В реальном приложении здесь должно быть логирование
        return Response(
            content=str({"detail": "Ошибка базы данных"}),
            status_code=500,
            media_type="application/json"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 