import pytest
from domain.users.value_objects.username import (
    MAX_USERNAME_LENGTH,
    EmptyUsernameError,
    TooLongUsernameError,
    Username,
    WrongUsernameFormatError,
)
from tests.exceptions import SuccessOrRaisesContext


class TestUsername:
    @pytest.mark.parametrize(
        ("username", "reference_context"),
        [
            ("user", SuccessOrRaisesContext()),
            ("user1234", SuccessOrRaisesContext()),
            ("1234", SuccessOrRaisesContext()),
            ("", SuccessOrRaisesContext(EmptyUsernameError)),
            ("0" * (MAX_USERNAME_LENGTH + 1), SuccessOrRaisesContext(TooLongUsernameError)),
            ("user,=", SuccessOrRaisesContext(WrongUsernameFormatError)),
        ],
    )
    def test_validate(self, username: str, reference_context: SuccessOrRaisesContext) -> None:
        with reference_context():
            Username(username)
