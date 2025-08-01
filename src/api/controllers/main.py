from api.controllers.healthcheck import router as healthcheck
from fastapi import FastAPI


def setup_controllers(app: FastAPI) -> None:
    app.include_router(healthcheck)
