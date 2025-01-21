.PHONY: up down build logs shell migrate

up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose build

logs:
	docker compose logs -f

shell:
	docker compose exec server bash

migrate:
	docker compose exec server alembic upgrade head

dev: build up migrate