import typing as t

from nextcord import Colour, Forbidden, HTTPException, Interaction, Permissions, SlashOption, User, slash_command
from nextcord.ext import application_checks

from . import BaseCog
from .pagination import PaginationView

if t.TYPE_CHECKING:
    from .. import Skurczybyk


class Moderation(BaseCog):
    def __init__(self, bot: "Skurczybyk") -> None:
        super().__init__(bot)

    @slash_command(description="Ban user", default_member_permissions=Permissions(ban_members=True))
    @application_checks.guild_only()
    async def ban(
        self,
        interaction: Interaction,
        user: User = SlashOption(description="Decide who should be banned"),
        reason: str = SlashOption(description="Describe ban reason", required=False, default="No reason given"),
        clear_messages: bool = SlashOption(
            description="Choose whether clear user's messages or not",
            choices={"Yes": True, "No": False},
            default=False,
            required=False,
        ),
    ):
        try:
            if user is None:
                await interaction.send("Something went wrong.", ephemeral=True)
                return
            if interaction.user == user:
                await interaction.send(f"{user.mention}, you can't ban yourself!", ephemeral=True)
                return
            if not clear_messages:
                await interaction.guild.ban(user=user, reason=reason, delete_message_seconds=0)
            else:
                await interaction.guild.ban(user=user, reason=reason, delete_message_seconds=604800)
            await interaction.send(f"{interaction.user.mention} banned {user.display_name}! Reason: {reason}")
        except Forbidden:
            await interaction.send(
                f"{interaction.user.mention}, you've got no permission to perform this command!", ephemeral=True
            )
        except HTTPException:
            await interaction.send(f"{interaction.user.mention}, banning failed.", ephemeral=True)

    @slash_command(description="Kick user", default_member_permissions=Permissions(kick_members=True))
    @application_checks.guild_only()
    async def kick(
        self,
        interaction: Interaction,
        user: User = SlashOption(description="Decide who should be kicked"),
        reason: str = SlashOption(description="Describe kick reason", required=False, default="No reason given"),
    ):
        try:
            if user is None:
                await interaction.send("Something went wrong.", ephemeral=True)
                return
            if interaction.user == user:
                await interaction.send(f"{interaction.user.mention}, you can't kick yourself!", ephemeral=True)
                return
            await interaction.guild.kick(user=user, reason=reason)
            await interaction.send(f"{interaction.user.mention} kicked {user.mention}! Reason: {reason}")
        except Forbidden:
            await interaction.send(
                f"{interaction.user.mention}, you've got no permission to perform this command!", ephemeral=True
            )
        except HTTPException:
            await interaction.send(f"{interaction.user.mention}, unbanning failed.", ephemeral=True)

    @slash_command(description="See banned users", default_member_permissions=Permissions(administrator=True))
    @application_checks.guild_only()
    async def bans(self, interaction: Interaction):
        ban_list: list[dict] = [{entry.user.name: entry.reason} async for entry in interaction.guild.bans()]

        data = []

        if ban_list:
            for entry in ban_list:
                data.append(*((f"• {name}", reason) for (name, reason) in entry.items()))
        else:
            data = [("", "No banned users")]

        bans_view = PaginationView(
            data,
            title="List of bans",
            description="See banned users and their banning reason.",
            color=Colour(0x1EA9FF),
            icon_url="https://lh3.googleusercontent.com/drive-viewer/AITFw-xNjHq5ShLIkWYl0hgoufXyOwwqBpceO_e--RolWCfXwlRBx1DWjwyZ6zcN48nm9r7ZmSSvDibtc3bBaBXExAx1urBr=w3024-h1514",
        )

        await bans_view.send(interaction=interaction)
    
    @slash_command(description="Unban user", default_member_permissions=Permissions(ban_members=True))
    @application_checks.guild_only()
    async def unban(
        self,
        interaction: Interaction,
        user: User,
    ):
        try:
            if user is None:
                await interaction.send("Something went wrong")
                return
            if interaction.user == user:
                await interaction.send(f"{user.mention}, you can't unban yourself", ephemeral=True)
                return
            await interaction.guild.unban(user)
            await interaction.send(f"{interaction.user.mention} unbanned {user.display_name}!")
        except Forbidden:
            await interaction.send(
                f"{interaction.user.mention}, you've got no permission to perform this command!", ephemeral=True
            )
        except HTTPException:
            await interaction.send(f"{interaction.user.mention}, unbanning failed.", ephemeral=True)
