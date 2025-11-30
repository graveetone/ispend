from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = "postgresql+asyncpg://{username}:{password}@{host}:{port}/{database}".format(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT", 5432),
    username=os.getenv("DB_USERNAME"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
)

Base = declarative_base()

engine = create_async_engine(DATABASE_URL, echo=True)


async_session_maker = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def create_db_with_tables(url):
    eng = create_async_engine(url, echo=True)
    async with eng.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
