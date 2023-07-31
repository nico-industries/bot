import os
import typing as t
from dataclasses import dataclass

from .errors import ConversionError, MissingEnvironmentVariable
from .utils import MISSING

__all__: tuple[str, ...] = ("Environment",)

T = t.TypeVar("T")


@dataclass(kw_only=True)
class Variable(t.Generic[T]):
    name: str
    default: t.Any = MISSING
    cast: t.Type[T] = MISSING

    def __post_init__(self) -> None:
        self.value = os.getenv(self.name, self.default)
        if self.value is MISSING:
            raise MissingEnvironmentVariable(self.name)

        if self.cast is not MISSING:
            try:
                self.value = self.cast(self.value)
            except Exception as e:
                raise ConversionError(self.name, self.cast, e) from e

    def __get__(self, instance: t.Any, owner: t.Any) -> T:
        return t.cast(T, self.value)


class Environment:
    TOKEN = Variable(name="TOKEN")
