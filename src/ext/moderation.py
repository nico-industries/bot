import typing as t

from nextcord import Interaction, Member, slash_command, Forbidden, HTTPException, SlashOption

from . import BaseCog

if t.TYPE_CHECKING:
    from .. import Skurczybyk


class Moderation(BaseCog):
    def __init__(self, bot: "Skurczybyk") -> None:
        super().__init__(bot)

    @slash_command(description="Ban user")
    async def ban(
        self,
        interaction: Interaction,
        member: Member,
        reason: str = SlashOption(name="reason", description="Banning reason", required=False),
        # clearMessages: str = SlashOption(
        #     name="clearMessages", description="Clear user's messages", required=False, choices={"yes": "y", "no": "n"}
        # ),
    ):
        if reason == None:
            reason = "No given reason"
        try:
            # delete_message_seconds = 604800
            await member.ban(reason=reason)
            await interaction.send(f"{interaction.user.mention} banned {member.mention}! Reason: {reason}")
        except Forbidden:
            await interaction.send(f"You've got no permission to perform this command!")
        except HTTPException:
            await interaction.send(f"Banning failed :(")
        finally:
            await interaction.send(f"Successfully banned {member.mention}", ephemeral=True)
