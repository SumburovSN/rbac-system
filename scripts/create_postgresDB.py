#!/usr/bin/env python3
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def create_db():
    db_name = "rbac_api"

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

create_db()