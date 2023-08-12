import typing as t

from nextcord import Interaction, Member, slash_command, Forbidden, HTTPException, SlashOption, Permissions

from . import BaseCog

if t.TYPE_CHECKING:
    from .. import Skurczybyk


class Moderation(BaseCog):
    def __init__(self, bot: "Skurczybyk") -> None:
        super().__init__(bot)

    @slash_command(description="Ban user", default_member_permissions=Permissions(8))
    async def ban(
        self,
        interaction: Interaction,
        member: Member,
        reason: str = SlashOption(description="Banning reason", required=False),
        clear_messages: str = SlashOption(
            description="Clear user's messages", choices=["True", "False"], default=False, required=False
        ),
    ):
        if not reason:
            reason = "No reason given"
        try:
            if clear_messages == "False":
                await member.ban(reason=reason)
                await interaction.send(f"{interaction.user.mention} banned {member.mention}! Reason: {reason}")
            else:
                delete_message_seconds = 604800  # week
                await member.ban(reason=reason, delete_message_seconds=delete_message_seconds)
                await interaction.send(f"{interaction.user.mention} banned {member.mention}! Reason: {reason}")
        except Forbidden:
            await interaction.send(f"You've got no permission to perform this command!")
        except HTTPException:
            await interaction.send(f"Banning failed.")
        finally:
            await interaction.send(f"Successfully banned {member.mention}", ephemeral=True)
