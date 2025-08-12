# db_create.py
import asyncio
import asyncpg
import os

from .db import create_db_with_tables

PG_USER = os.getenv("PGUSER", "postgres")
PG_PASS = os.getenv("PGPASSWORD", "mysecretpassword")
PG_HOST = os.getenv("PGHOST", "localhost")
PG_PORT = os.getenv("PGPORT", "5432")
DB_NAME = os.getenv("PGDATABASE", "ispend_db_test")


async def ensure_database(db_name=DB_NAME, force_drop=False):
    conn = await asyncpg.connect(
        user=PG_USER,
        password=PG_PASS,
        host=PG_HOST,
        port=PG_PORT,

        database="postgres"  # connect to default
    )
    db_exists = await conn.fetchval("SELECT 1 FROM pg_database WHERE datname=$1", db_name)
    if db_exists:
        if not force_drop:
            return

        await conn.execute(f'DROP DATABASE "{db_name}"')

    await conn.execute(f'CREATE DATABASE "{db_name}"')
    await create_db_with_tables(f"postgresql+asyncpg://{PG_USER}:{PG_PASS}@{PG_HOST}/{db_name}")
    await conn.close()


async def drop_database():
    conn = await asyncpg.connect(
        user=PG_USER,
        password=PG_PASS,
        host=PG_HOST,
        port=PG_PORT,
        database="postgres"  # connect to default
    )
    db_exists = await conn.fetchval("SELECT 1 FROM pg_database WHERE datname=$1", DB_NAME)
    if db_exists:
        await conn.execute(f'DROP DATABASE "{DB_NAME}"')
    print(f"Database '{DB_NAME}' dropped.")
    await conn.close()


if __name__ == "__main__":
    asyncio.run(ensure_database())
