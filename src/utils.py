import typing as t

__all__: tuple[str, ...] = ("MISSING",)


class _MissingSentinel:
    def __eq__(self, other: t.Any) -> bool:
        return self is other

    def __hash__(self) -> int:
        return id(self)

    def __bool__(self) -> bool:
        return False

    def __repr__(self) -> str:
        return "..."


MISSING: t.Any = _MissingSentinel()
