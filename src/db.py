# from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.pool import StaticPool


DATABASE_URL = "postgresql+asyncpg://postgres:mysecretpassword@localhost/test_db"

engine = AsyncEngine(
    create_async_engine(
        url=DATABASE_URL,
        echo=True,
    )
)


async def init_db():
    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    Session = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        poolclass=StaticPool,
    )
    async with Session() as session:
        yield session

