#!/usr/bin/make

include deploy/.env.dev

export PYTHONPATH=:$(PWD)/code_:$(PWD)/code_/app
export FLASK_APP=manage.py

help:
	@echo "make"
	@echo "	hello"
	@echo "		print hello world"

hello:
	echo "Hello, World"
alembic-init:
	flask db init -d code_/alembic
alembic-head:
	flask db upgrade -d code_/alembic head
alembic-revision:
	flask db revision -d code_/alembic --autogenerate -m '$(ARGS)'
alembic-downgrade:
	flask db downgrade -d code_/alembic
docker-build:
	docker compose -f deploy/docker-compose.yml --env-file=deploy/.env.prod build
docker-up:
	docker compose -f deploy/docker-compose.yml --env-file=deploy/.env.prod up -d --build
docker-down:
	docker compose -f deploy/docker-compose.yml --env-file=deploy/.env.prod down