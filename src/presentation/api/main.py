import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from mediator import Mediator
from presentation.api.controllers.main import setup_controllers
from presentation.api.middlewares.main import setup_middlewares
from presentation.api.setup_providers import setup_providers
from settings import settings

logger = logging.getLogger()


def init_api(*, mediator: Mediator, debug: bool = __debug__) -> FastAPI:
    logger.info("Initialize API")
    app = FastAPI(
        debug=debug,
        title="User service",
        version="1.0.0",
        default_response_class=ORJSONResponse,
    )
    setup_middlewares(app)
    setup_controllers(app)
    setup_providers(app, mediator)
    return app


async def run_api(app: FastAPI) -> None:
    config = uvicorn.Config(
        app,
        host=settings.api.host,
        port=settings.api.port,
        log_level=logging.INFO,
        log_config=None,
    )
    server = uvicorn.Server(config)
    await server.serve()
