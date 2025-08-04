from fastapi import FastAPI
from presentation.api.middlewares.logs import set_request_id_middleware
from starlette.middleware.base import BaseHTTPMiddleware


def setup_middlewares(app: FastAPI) -> None:
    app.add_middleware(BaseHTTPMiddleware, dispatch=set_request_id_middleware)
