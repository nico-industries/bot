import typing as t

from nextcord import Forbidden, HTTPException, Interaction, Member, Permissions, SlashOption, User, slash_command

from . import BaseCog

if t.TYPE_CHECKING:
    from .. import Skurczybyk


class Moderation(BaseCog):
    def __init__(self, bot: "Skurczybyk") -> None:
        super().__init__(bot)

    @slash_command(description="Ban user", default_member_permissions=Permissions(administrator=True))
    async def ban(
        self,
        interaction: Interaction,
        member: Member,
        reason: str = SlashOption(description="Banning reason", required=False, default="No reason given"),
        clear_messages: str = SlashOption(
            description="Clear user's messages",
            choices=["Yes", "No"],
            default="No",
            required=False,
        ),
    ):
        try:
            if clear_messages == "No":
                await member.ban(reason=reason, delete_message_seconds=0)
                await interaction.send(f"{interaction.user.mention} banned {member.mention}! Reason: {reason}")
            else:
                await member.ban(reason=reason, delete_message_seconds=604800)
                await interaction.send(f"{interaction.user.mention} banned {member.mention}! Reason: {reason}")
        except Forbidden:
            await interaction.send(f"You've got no permission to perform this command!")
        except HTTPException:
            await interaction.send(f"Banning failed.")
        finally:
            await interaction.send(f"Successfully banned {member.mention}", ephemeral=True)
