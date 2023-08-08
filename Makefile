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
