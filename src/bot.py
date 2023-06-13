import importlib
import inspect
import pathlib
import typing as t

import aiohttp
import nextcord
from nextcord.ext import commands
from prisma import Prisma

from .env import Environment
from .logger import Logger

__all__: tuple[str, ...] = ("Skurczybyk",)


class Skurczybyk(commands.Bot):
    def __init__(self) -> None:
        self.logger = Logger(name="Skurczybyk")
        self.http_session = aiohttp.ClientSession()
        self.config = Environment()
        self.prisma = Prisma()
        super().__init__(command_prefix=".", intents=nextcord.Intents.all())

    async def on_ready(self) -> None:
        self.logger.info(f"Logged in as {self.user} ({self.user.id})")

    async def close(self) -> None:
        self.logger.info("Closing...")
        await self.http_session.close()
        await self.prisma.disconnect()
        await super().close()
        self.logger.info("Closed!")

    def _auto_setup(self, path: str) -> None:
        module = importlib.import_module(path)
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and issubclass(obj, commands.Cog) and name != "BaseCog":
                self.add_cog(obj(self))
                self.logger.info(f"Loaded {name} cog.")

    def _load_all_extensions(self) -> None:
        self.logger.info("Loading extensions...")
        extensions = pathlib.Path("src/ext")
        for path in extensions.glob("*.py"):
            if path.name.startswith("_"):
                continue
            self._auto_setup(f"{extensions.parent}.{extensions.name}.{path.stem}")
        self.logger.info("Loaded all extensions!")

    def run(self, *args: t.Any, **kwargs: t.Any) -> None:
        self.loop.run_until_complete(self.prisma.connect())
        self._load_all_extensions()
        self.logger.info("Starting...")
        try:
            super().run(self.config.TOKEN, *args, **kwargs)
        except Exception:
            self.logger.critical("Failed to run bot!")
            self.logger.info("Closing...")

    @property
    def user(self) -> nextcord.ClientUser:
        assert super().user
        return super().user
