import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_DIR = ROOT / "app"

def run(cmd, cwd=None):
    print(f"> {' '.join(cmd)}")
    subprocess.check_call(cmd, cwd=cwd)

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
    run([sys.executable, "scripts/create_postgres_db.py"], cwd=ROOT)

    # 3. alembic upgrade
    run(["alembic", "upgrade", "head"], cwd=APP_DIR)

    print("🎉 Project initialized successfully")

if __name__ == "__main__":
    main()
