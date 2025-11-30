import asyncio
import asyncpg
import os

from dotenv import load_dotenv

from .db import create_db_with_tables

load_dotenv()
PG_USER = os.getenv("DB_USERNAME")
PG_PASS = os.getenv("DB_PASSWORD")
PG_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")


async def ensure_database(force_drop=True):
    if not all((PG_HOST, PG_PASS, PG_HOST, DB_NAME)):
        raise ValueError("Missing database credentials")

    conn = await asyncpg.connect(
        user=PG_USER,
        password=PG_PASS,
        host=PG_HOST,
        port=5432,
        database="postgres"  # connect to default
    )
    db_exists = await conn.fetchval(
        "SELECT 1 FROM pg_database WHERE datname=$1", DB_NAME
    )
    if db_exists and force_drop and not os.getenv("ENV") == "prod":
        await conn.execute(f'DROP DATABASE "{DB_NAME}"')

        await conn.execute(f'CREATE DATABASE "{DB_NAME}"')

        await create_db_with_tables(
            f"postgresql+asyncpg://{PG_USER}:{PG_PASS}@{PG_HOST}/{DB_NAME}"
        )
    await conn.close()


if __name__ == "__main__":
    asyncio.run(ensure_database())
