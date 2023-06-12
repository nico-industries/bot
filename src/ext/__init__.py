import typing as t

from nextcord.ext import commands

if t.TYPE_CHECKING:
    from .. import Skurczybyk

__all__: tuple[str, ...] = ("BaseCog",)


class BaseCog(commands.Cog):
    def __init__(self, bot: "Skurczybyk") -> None:
        self.bot = bot
        self.logger = bot.logger
        self.http = bot.http_session
        self.prisma = bot.prisma
