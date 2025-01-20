# scripts/start.sh
#!/bin/bash
set -e

# Wait for a few seconds to ensure database is ready (more important for PostgreSQL/MySQL)
sleep 2

# Create initial migration if no migrations exist
if [ -z "$(ls -A app/migrations/versions/)" ]; then
    echo "No migrations found. Creating initial migration..."
    alembic revision --autogenerate -m "Initial migration"
fi

# Run migrations
echo "Running database migrations..."
alembic upgrade head

# Start the application

echo "Starting FastAPI application in production mode..."
uvicorn app.main:app --host 0.0.0.0 --port 8000
