# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7

ARG PYTHON_VERSION=3.12.3
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-privileged user and set up directories
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/home/appuser" \
    --shell "/bin/bash" \
    --uid "1000" \
    appuser && \
    mkdir -p /app/logs /home/appuser/.cache/huggingface && \
    chown -R appuser:appuser /app /home/appuser && \
    chmod -R 777 /app/logs /home/appuser/.cache/huggingface

# Copy configuration files first
COPY alembic.ini .
COPY alembic/ ./alembic/
COPY scripts/ ./scripts/

# Set proper permissions for the entrypoint script
RUN chmod +x scripts/entrypoint.sh && \
    chown -R appuser:appuser scripts/

# Download dependencies
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Set the proper working directory
WORKDIR /app

# Copy the source code and set permissions
COPY --chown=appuser:appuser . .
RUN chmod +x scripts/entrypoint.sh

# Switch to non-privileged user
USER appuser

# Expose port and set entrypoint
EXPOSE 8000
ENTRYPOINT ["./scripts/entrypoint.sh"]
