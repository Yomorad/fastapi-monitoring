#!/bin/bash

# Ожидание, чтобы база данных успела подняться
sleep 5

echo "Applying migrations..."
alembic revision --autogenerate -m "init migration"
alembic upgrade head
echo "Migrations applied successfully."
