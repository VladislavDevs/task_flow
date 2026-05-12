from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from backend.app.core.config import settings

# Движок SQLAlchemy для PostgreSQL
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,      # проверять соединение перед использованием
    pool_size=10,            # базовый размер пула
    max_overflow=20,         # дополнительные соединения при превышении pool_size
    echo=False               # установите True для отладки SQL-запросов
)

# Фабрика сессий, привязанная к движку
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Базовый класс для декларативных моделей SQLAlchemy
# Все модели ORM будут наследоваться от него
Base = declarative_base()

# Генератор зависимости FastAPI для получения сессии БД
def get_db():
    """
    Создаёт сессию, выполняет запрос и гарантированно закрывает её.
    Используется как зависимость в эндпоинтах FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()