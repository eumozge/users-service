import logging

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from settings import settings

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def init(*, debug: bool = __debug__) -> FastAPI:
    logger.debug("Initialize API")
    return FastAPI(
        debug=debug,
        title="User service",
        version="1.0.0",
        default_response_class=ORJSONResponse,
    )


async def run(app: FastAPI) -> None:
    config = uvicorn.Config(
        app,
        host=settings.api.host,
        port=settings.api.port,
        log_level=logging.INFO,
        log_config=None,
    )
    server = uvicorn.Server(config)
    logger.info("Running API")
    await server.serve()
