from fastapi import FastAPI
from presentation.api.controllers.healthcheck import router as healthcheck
from presentation.api.controllers.users import router as users
from presentation.api.exeptions import setup_exception_handlers


def setup_controllers(app: FastAPI) -> None:
    app.include_router(healthcheck)
    app.include_router(users)
    setup_exception_handlers(app)
