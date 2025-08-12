import logging
from collections.abc import Awaitable, Callable
from functools import partial

from app.users.exceptions import UserIdAlreadyExistsError, UserIdNotExistError, UsernameNotExistError
from domain.common.exceptions import AppError
from domain.users.exeptions import UsernameAlreadyExistsError
from domain.users.value_objects.username import (
    UsernameValueError,
)
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from presentation.api.controllers.responses.base import ErrorData, ErrorResponse
from starlette import status
from starlette.requests import Request

logger = logging.getLogger(__name__)


def setup_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, error_handler(status.HTTP_500_INTERNAL_SERVER_ERROR))
    app.add_exception_handler(UserIdNotExistError, error_handler(status.HTTP_404_NOT_FOUND))
    app.add_exception_handler(UsernameNotExistError, error_handler(status.HTTP_404_NOT_FOUND))
    app.add_exception_handler(UsernameValueError, error_handler(status.HTTP_400_BAD_REQUEST))
    app.add_exception_handler(UserIdAlreadyExistsError, error_handler(status.HTTP_409_CONFLICT))
    app.add_exception_handler(UsernameAlreadyExistsError, error_handler(status.HTTP_409_CONFLICT))
    app.add_exception_handler(Exception, unknown_exception_handler)


def error_handler(status_code: int) -> Callable[..., Awaitable[ORJSONResponse]]:
    return partial(app_error_handler, status_code=status_code)


async def app_error_handler(request: Request, err: AppError, status_code: int) -> ORJSONResponse:
    return await handle_error(
        request=request,
        err=err,
        err_data=ErrorData(data=err),
        status=err.status,
        status_code=status_code,
    )


async def unknown_exception_handler(
    request: Request,  # noqa: ARG001 Unused function argument: `request`
    err: Exception,
) -> ORJSONResponse:
    logger.error("Handle error", exc_info=err, extra={"error": err})
    logger.exception("Unknown error occurred", exc_info=err, extra={"error": err})
    return ORJSONResponse(
        ErrorResponse(error=ErrorData(data=err)),
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


async def handle_error(
    request: Request,  # noqa: ARG001 Unused function argument: `request`
    err: Exception,
    err_data: ErrorData,
    status: int,
    status_code: int,
) -> ORJSONResponse:
    logger.error("Handle error", exc_info=err, extra={"error": err})
    return ORJSONResponse(
        ErrorResponse(error=err_data, status=status),
        status_code=status_code,
    )
