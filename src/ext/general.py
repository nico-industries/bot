import typing as t

from . import BaseCog

if t.TYPE_CHECKING:
    from .. import Skurczybyk


class General(BaseCog):
    def __init__(self, bot: "Skurczybyk") -> None:
        super().__init__(bot)
