import os
import typing as t
from dataclasses import dataclass

from .errors import ConversionError, MissingEnvironmentVarriable
from .utils import MISSING

__all__: tuple[str, ...] = ("Environment",)


@dataclass(kw_only=True)
class Varriable:
    name: str
    default: t.Any = MISSING
    cast: t.Callable[[str], t.Any] = str

    def __post_init__(self) -> None:
        self.value = os.getenv(self.name, self.default)
        if self.value is MISSING:
            raise MissingEnvironmentVarriable(self.name)

        if self.cast is str:
            return

        try:
            self.value = self.cast(self.value)
        except Exception as e:
            raise ConversionError(self.name, self.cast, e) from e

    def __str__(self) -> str:
        if self.cast is str:
            return self.value
        return str(super())

    def __get__(self, instance: t.Any, owner: t.Any) -> cast:
        return self.value


class Environment:
    TOKEN = Varriable(name="TOKEN")
