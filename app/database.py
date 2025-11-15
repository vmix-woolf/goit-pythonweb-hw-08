from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
)

# Фабрика асинхронних сесій
SessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
)

# Базовий клас для моделей ORM
class Base(DeclarativeBase):
    pass

# Залежність FastAPI — генерує сесію для кожного запиту
async def get_db():
    async with SessionLocal() as session:
        yield session
