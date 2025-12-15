import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

import asyncio
from app.domain.repositories.session_repository_redis import SessionRepositoryRedis
from app.infrastructure.redis_client import redis_client
from app.use_cases.session_service import SessionService


def create_db():
    db_name = "my_new_db"

    # Подключаемся к существующей БД "postgres"
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="postgres",
        host="localhost",
        port=5432
    )

    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    # Проверяем наличие базы данных
    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (db_name,))
    exists = cur.fetchone()

    if exists:
        print(f"База '{db_name}' уже существует.")
    else:
        cur.execute(f"CREATE DATABASE {db_name};")
        print(f"База '{db_name}' создана.")

    cur.close()
    conn.close()

async def get_session_service():
    client = redis_client
    repo = SessionRepositoryRedis(client)
    service = SessionService(repo)
    session = await service.create_session(user_id=1, ip="127:0:", user_agent="Chrome")
    print(session)

asyncio.run(get_session_service())

