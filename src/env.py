import os
import typing as t
from dataclasses import dataclass
from functools import cached_property

from .errors import ConversionError, MissingEnvironmentVariable
from .utils import MISSING

__all__: tuple[str, ...] = ("Environment",)

T = t.TypeVar("T")


@dataclass(kw_only=True)
class Variable(t.Generic[T]):
    name: str
    default: T = MISSING
    cast: type[T] = MISSING

    @cached_property
    def value(self) -> T:
        _value = os.getenv(self.name, self.default)
        if _value is MISSING:
            raise MissingEnvironmentVariable(self.name)

        if self.cast is not MISSING:
            try:
                _value = self.cast(_value)
            except Exception as e:
                raise ConversionError(self.name, self.cast, e) from e

        return t.cast(T, _value)

    def __get__(self, instance: t.Any, owner: t.Any) -> T:
        return self.value


class Environment:
    TOKEN = Variable(name="TOKEN")
    LOG_CHANNEL_ID = Variable(name="LOG_CHANNEL_ID", cast=int)
