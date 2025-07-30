package_dir := "src"

py *args:
    uv run {{args}}

help:
    just -l

install:
    uv run pre-commit install && uv sync --all-extras --all-groups

lint:
    just py pre-commit run --all-files

test *args:
    just py pytest {{args}}
