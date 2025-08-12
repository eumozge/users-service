from fastapi import FastAPI
from mediator import Mediator


def setup_providers(app: FastAPI, mediator: Mediator) -> None:
    app.state.mediator = mediator
