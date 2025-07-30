package_dir := "src"

_py *args:
    uv run {{args}}

help:
    just -l

install:
    uv run pre-commit install && uv sync --all-extras --all-groups

lint:
    just _py pre-commit run --all-files

test *args:
    just _py pytest {{args}}
