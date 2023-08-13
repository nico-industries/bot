import typing as t
from datetime import timedelta

from nextcord import Forbidden, HTTPException, Interaction, Permissions, SlashOption, User, slash_command
from nextcord.ext import application_checks

from . import BaseCog

if t.TYPE_CHECKING:
    from .. import Skurczybyk


class Moderation(BaseCog):
    def __init__(self, bot: "Skurczybyk") -> None:
        super().__init__(bot)

    @slash_command(description="Ban user", default_member_permissions=Permissions(administrator=True))
    @application_checks.guild_only()
    async def ban(
        self,
        interaction: Interaction,
        user: User,
        reason: str = SlashOption(description="Banning reason", required=False, default="No reason given"),
        clear_messages: bool = SlashOption(
            description="Clear user's messages",
            choices={"Yes": True, "No": False},
            default=False,
            required=False,
        ),
    ):
        try:
            if clear_messages == False:
                await interaction.guild.ban(user=user, reason=reason, delete_message_seconds=0)
            else:
                await interaction.guild.ban(user=user, reason=reason, delete_message_seconds=604800)
            await interaction.send(f"{interaction.user.mention} banned {user.display_name}! Reason: {reason}")
        except Forbidden:
            await interaction.send(f"{interaction.user.mention}, you've got no permission to perform this command!")
        except HTTPException:
            await interaction.send(f"{interaction.user.mention}, banning failed.", ephemeral=True)
