from contextlib import nullcontext
from dataclasses import dataclass

import pytest


@dataclass
class SuccessOrRaisesContext:
    exception: None | type[Exception] = None

    def __call__(self):
        return pytest.raises(self.exception) if self.exception is not None else nullcontext()
