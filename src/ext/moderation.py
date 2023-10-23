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
        user_name: str = SlashOption(name="user", description="Decide who should be unbanned"),
    ):
        try:
            if not user_name:
                await interaction.send("Something went wrong.", ephemeral=True)
                return
            if interaction.user.name == user_name:
                await interaction.send(f"{interaction.user.mention}, you can't unban yourself!", ephemeral=True)
                return

            banned_users: list[User] = [entry.user async for entry in interaction.guild.bans()]
            banned_users_names: dict[str, User] = self.get_user_by_username(banned_users)

            banned_user: User = banned_users_names.get(user_name)
            if banned_user is None:
                await interaction.send(f"{interaction.user.mention}, user not found!", ephemeral=True)
                return
            await interaction.guild.unban(banned_user)
            await interaction.send(f"{interaction.user.mention} unbanned {banned_user.mention}!")

        except Forbidden:
            await interaction.send(
                f"{interaction.user.mention}, you've got no permission to perform this command!", ephemeral=True
            )
        except HTTPException:
            await interaction.send(f"{interaction.user.mention}, unbanning failed.", ephemeral=True)

    def get_user_by_username(self, list_of_users: list[User]) -> dict[str, User]:
        return {user.name: user for user in list_of_users}

    @unban.on_autocomplete("user_name")
    async def banned_user(self, interaction: Interaction, user: str):
        banned_users_names: list[str] = [entry.user.name async for entry in interaction.guild.bans()]

        if not user:
            await interaction.response.send_autocomplete(banned_users_names)
            return

        get_near_banned_user: list[str] = [
            banned_user_name
            for banned_user_name in banned_users_names
            if banned_user_name.lower().startswith(user.lower())
        ]

        await interaction.response.send_autocomplete(get_near_banned_user)
