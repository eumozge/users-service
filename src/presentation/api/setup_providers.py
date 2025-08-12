from di import DI
from fastapi import FastAPI
from mediator import Mediator


def setup_providers(app: FastAPI, mediator: Mediator, di: DI) -> None:
    app.state.mediator = mediator
    app.state.di = di
