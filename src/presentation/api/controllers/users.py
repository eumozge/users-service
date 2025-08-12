from typing import Annotated

from app.users.commands import CreateUser
from app.users.exceptions import UserIdAlreadyExistsError
from di import DI
from domain.users.exeptions import UsernameAlreadyExistsError
from domain.users.value_objects.username import EmptyUsernameError, TooLongUsernameError, WrongUsernameFormatError
from fastapi import APIRouter, Depends, status
from mediator import Mediator
from presentation.api.controllers.depends.mediator import get_di, get_mediator
from presentation.api.controllers.responses.base import ErrorResponse, OkResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "",
    name="create_user",
    responses={
        status.HTTP_201_CREATED: {"model": OkResponse[None]},
        status.HTTP_400_BAD_REQUEST: {
            "model": ErrorResponse[TooLongUsernameError | EmptyUsernameError | WrongUsernameFormatError],
        },
        status.HTTP_409_CONFLICT: {
            "model": ErrorResponse[UsernameAlreadyExistsError | UserIdAlreadyExistsError],
        },
    },
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    create_user_command: CreateUser,
    di: Annotated[DI, Depends(get_di)],
    mediator: Annotated[Mediator, Depends(get_mediator)],
) -> OkResponse[None]:
    async with di.db_session_maker()() as db_session:
        await mediator.handle_command(
            command=create_user_command,
            user_service=di.user_service(user_repository=di.user_repository(session=db_session)),
            uow=di.db_uow(session=db_session),
        )

    return OkResponse(status.HTTP_201_CREATED)
