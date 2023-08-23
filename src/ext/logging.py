import traceback
import typing as t
from io import StringIO

import nextcord
from nextcord.ext import commands
from nextcord.utils import format_dt

from . import BaseCog

if t.TYPE_CHECKING:
    from .. import Skurczybyk


class Logging(BaseCog):
    def __init__(self, bot: "Skurczybyk") -> None:
        super().__init__(bot)

    @commands.Cog.listener("on_command_error")
    @commands.Cog.listener("on_application_command_error")
    async def log_exceptions(self, context: commands.Context | nextcord.Interaction, exception: Exception):
        if isinstance(exception, commands.CommandNotFound):
            return

        if not isinstance(context, commands.Context | nextcord.Interaction):
            raise TypeError(f"Unknown context type: {type(context)}")

        if isinstance(exception, commands.CommandError):
            exception = exception.original

        if isinstance(context, commands.Context):
            invoker = context.author
            created_at = context.message.created_at
            name = f"`{context.command.qualified_name}`"
            _args = context.args[2:]  # ignore self and ctx
            _kwargs = context.kwargs

            args = " ".join(_args + [f"{k}={v}" for k, v in _kwargs.items()])

        elif isinstance(context, nextcord.Interaction):
            invoker = context.user
            created_at = context.created_at
            name = context.application_command.get_mention()
            _options = context.data.get("options")

            args = " ".join(f"{option['name']}={option['value']}" for option in _options)

        guild = context.guild
        channel = context.channel

        embed = (
            nextcord.Embed(
                title="Exception occured!",
                color=nextcord.Color.red(),
                timestamp=created_at,
            )
            .add_field(
                name="Invokation details",
                value=(
                    "```yaml\n"
                    f"Guild: {guild.name} ({guild.id})\n"
                    f"Channel: {channel.name} ({channel.id})\n"
                    f"Invoker: {invoker.name} ({invoker.id})\n"
                    "```"
                ),
                inline=False,
            )
            .add_field(
                name="Command details",
                value=(
                    f"**Command**: {name}\n"
                    f"**Arguments**: `{args if args else None}`\n"
                    f"**Executed at**: {format_dt(created_at)} ({format_dt(created_at, style='R')})"
                ),
                inline=False,
            )
        )

        tb = "".join(traceback.format_exception(type(exception), exception, exception.__traceback__))

        _LOG_CHANNEL_ID = self.bot.config.LOG_CHANNEL_ID
        _log_channel = self.bot.get_channel(_LOG_CHANNEL_ID) or await self.bot.fetch_channel(_LOG_CHANNEL_ID)

        if len(tb) < 4000:
            embed.description = f"```py\n{tb}```"
            await _log_channel.send(embed=embed)
            return

        await _log_channel.send(
            "Traceback is too long. Uploading as a file.",
            embed=embed,
            file=nextcord.File(StringIO(tb), filename="traceback.txt"),
        )
