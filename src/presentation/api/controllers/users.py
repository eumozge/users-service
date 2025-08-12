from typing import Annotated

from app.users.commands import CreateUser
from app.users.exceptions import UserIdAlreadyExistsError
from domain.users.exeptions import UsernameAlreadyExistsError
from domain.users.services import UserService
from domain.users.value_objects.username import EmptyUsernameError, TooLongUsernameError, WrongUsernameFormatError
from fastapi import APIRouter, Depends, status
from infra.db.main import get_sa_session_maker
from infra.db.repositories.users import UserRepositoryImpl
from infra.db.uow import SQLAlchemyUoW
from mediator import Mediator
from presentation.api.controllers.depends.mediator import get_mediator
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
    mediator: Annotated[Mediator, Depends(get_mediator)],
) -> OkResponse[None]:
    """TODO get depends via DI or native depends."""
    async with get_sa_session_maker(engine=mediator.di.db_engine())() as session:
        uow = SQLAlchemyUoW(session=session)
        user_service = UserService(user_repository=UserRepositoryImpl(session=session))
        await mediator.handle_command(command=create_user_command, user_service=user_service, uow=uow)

    return OkResponse(status.HTTP_201_CREATED)
