import shutil
import subprocess
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_DIR = ROOT / "app"

def run(cmd, cwd=None):
    print(f"> {' '.join(cmd)}")
    subprocess.check_call(cmd, cwd=cwd)

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

def main():
    print("🚀 Initializing project...")

    # 1. .env
    env = APP_DIR / ".env"
    example = APP_DIR / "example.env"

    if not env.exists():
        shutil.copy(example, env)
        print("✅ .env created from example.env")
    else:
        print("ℹ️ .env already exists")

    # 2. create DB
    # run([sys.executable, "scripts/create_postgres_db.py"], cwd=ROOT)
    create_db()

    # 3. alembic upgrade
    run(["alembic", "upgrade", "head"], cwd=APP_DIR)

    print("🎉 Project initialized successfully")

if __name__ == "__main__":
    main()
