from fastapi import FastAPI
from presentation.api.controllers.healthcheck import router as healthcheck


def setup_controllers(app: FastAPI) -> None:
    app.include_router(healthcheck)
