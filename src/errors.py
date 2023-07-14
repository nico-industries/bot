import typing as t

from nextcord.ext import commands

__all__: tuple[str, ...] = (
    "MissingEnvironmentVarriable",
    "ConversionError",
)


class SkurczybykException(commands.CommandError):
    ...


class MissingEnvironmentVarriable(SkurczybykException):
    def __init__(self, name: str) -> None:
        self.name = name
        super().__init__(str(self))

    def __str__(self) -> str:
        return f"Missing environment variable: {self.name}"


class ConversionError(SkurczybykException):
    def __init__(self, name: str, value: t.Any, error: Exception) -> None:
        self.name = name
        self.value = value
        self.error = error
        super().__init__(str(self))

    def __str__(self) -> str:
        return f"Failed to convert {self.name} to {self.value.__qualname__}: {self.error}"
