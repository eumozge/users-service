from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

V = TypeVar("V", bound=Any)


@dataclass(frozen=True)
class BaseValueObject(ABC):
    def __post_init(self) -> None:
        self.validate()

    @abstractmethod
    def validate(self) -> None: ...


class ValueObject(BaseValueObject, Generic[V]):
    value: V

    def to_representative(self) -> V:
        return self.value
