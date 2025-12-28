#!/bin/sh
set -e

echo "Waiting for Postgres..."
while ! nc -z postgres 5432; do
  sleep 1
done

echo "Waiting for Redis..."
while ! nc -z redis 6379; do
  sleep 1
done

echo "Running Alembic migrations..."
alembic upgrade head

echo "Starting FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
