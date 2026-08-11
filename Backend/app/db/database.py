from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import settings

# 1. Create the Async Engine
engine = create_async_engine(settings.DATABASE_URL, echo=False)

# 2. Create the Async Session Factory
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

# 3. Base class for all your models
Base = declarative_base()

# 4. The FastAPI Dependency (moved from session.py)
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
