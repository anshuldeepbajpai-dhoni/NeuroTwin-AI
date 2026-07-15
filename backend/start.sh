#!/bin/sh

set -e

echo "Starting NeuroTwin deployment..."

echo "Running database migrations..."

alembic upgrade head

echo "Starting FastAPI server..."

exec uvicorn app.main:app \
    --host "${HOST:-0.0.0.0}" \
    --port "${PORT:-8000}" \
    --proxy-headers \
    --forwarded-allow-ips="*"