API := "src"
STORAGES := "dockercompose/dev.storages.yaml"
PROJECT_NAME := "users_service"

ENV := "--env-file .env"

py *args:
    uv run {{args}}

help:
    just -l

install:
    uv run pre-commit install && uv sync --all-extras --all-groups && export PYTHONPATH=$PYTHONPATH:$(pwd)/src

lint:
    just py pre-commit run --all-files

test *args:
    just py pytest {{args}}

migrations-make message="":
    uv run alembic revision --autogenerate -m "{{message}}"

migrations-apply:
    uv run alembic upgrade head

storages:
    docker compose -f {{STORAGES}} {{ENV}} -p {{ PROJECT_NAME }} up -d --remove-orphans

storages-logs:
    docker compose -f {{STORAGES}} {{ENV}} -p {{ PROJECT_NAME }} up --remove-orphans

storages-down:
	docker compose -f {{STORAGES}} {{ENV}} -p {{ PROJECT_NAME }} down

up:
	uv run python {{API}}
