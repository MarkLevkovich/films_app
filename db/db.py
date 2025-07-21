from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = 'postgresql+asyncpg://mark:Mark2410@localhost:5432/films_db'

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


class Base(DeclarativeBase):
    pass

async def get_db():
    async with async_session_maker() as session:
        yield session