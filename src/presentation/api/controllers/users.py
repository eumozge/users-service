from app.users.commands import CreateUser
from app.users.exceptions import UserIdAlreadyExistsError
from domain.users.exeptions import UsernameAlreadyExistsError
from domain.users.value_objects.username import EmptyUsernameError, TooLongUsernameError, WrongUsernameFormatError
from fastapi import APIRouter, status
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
async def create_user(create_user_command: CreateUser) -> OkResponse[None]:  # noqa: ARG001 Unused function argument: `create_user_command`
    """TODO Provide user creating after adding mediator."""
    return OkResponse(status.HTTP_201_CREATED)
