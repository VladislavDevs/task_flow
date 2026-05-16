from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Асинхронный движок SQLAlchemy для PostgreSQL
engine = create_async_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    echo=False
)

# Фабрика асинхронных сессий
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False
)

# Базовый класс для моделей
Base = declarative_base()

# Генератор зависимости FastAPI для получения сессии БД
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()