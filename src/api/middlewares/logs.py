from collections.abc import Awaitable, Callable
from contextvars import ContextVar
from uuid import uuid4

from fastapi import Request, Response

request_id: ContextVar[str] = ContextVar("request_id", default="")


def get_request_id() -> str:
    return request_id.get() or ""


def set_request_id(value: str) -> None:
    request_id.set(value)


async def set_request_id_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    set_request_id(request.headers.get("X-Request-ID") or str(uuid4()))

    request.state.request_id = get_request_id()

    response = await call_next(request)

    response.headers["X-Request-ID"] = get_request_id()
    return response
