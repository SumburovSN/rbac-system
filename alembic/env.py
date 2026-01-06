import sys
from pathlib import Path
from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine

# ============================================================
# Добавляем корень проекта в PYTHONPATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# ============================================================
# Импорты приложения
# ============================================================

from app.config import DATABASE_URL
from app.infrastructure.db.base import Base
import app.infrastructure.db.models  # noqa: F401

# ============================================================
# Alembic config
# ============================================================

config = context.config

if config.config_file_name:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# ============================================================
# Offline migrations
# ============================================================

def run_migrations_offline() -> None:
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()

# ============================================================
# Online migrations
# ============================================================

def run_migrations_online() -> None:
    engine = create_engine(DATABASE_URL)

    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()

# ============================================================
# Entrypoint
# ============================================================

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
