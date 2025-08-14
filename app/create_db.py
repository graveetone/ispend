import asyncio
import asyncpg
import os

from .db import create_db_with_tables

PG_USER = os.getenv("PGUSER", "postgres")
PG_PASS = os.getenv("PGPASSWORD", "mysecretpassword")
PG_HOST = os.getenv("PGHOST", "localhost")
PG_PORT = os.getenv("PGPORT", "5432")
DB_NAME = os.getenv("PGDATABASE", "ispend_db")


async def ensure_database():
    conn = await asyncpg.connect(
        user=PG_USER,
        password=PG_PASS,
        host=PG_HOST,
        port=PG_PORT,

        database="postgres"  # connect to default
    )
    db_exists = await conn.fetchval(
        "SELECT 1 FROM pg_database WHERE datname=$1", DB_NAME
    )
    if db_exists:
        await conn.execute(f'DROP DATABASE "{DB_NAME}"')

    await conn.execute(f'CREATE DATABASE "{DB_NAME}"')

    await create_db_with_tables(
        f"postgresql+asyncpg://{PG_USER}:{PG_PASS}@{PG_HOST}/{DB_NAME}"
    )
    await conn.close()


if __name__ == "__main__":
    asyncio.run(ensure_database())
