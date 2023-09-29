from datetime import datetime
from math import ceil
from typing import Tuple

from nextcord import ButtonStyle, Colour, Embed, Interaction, ui


class PaginationView(ui.View):
    current_page: int = 1

    def __init__(
        self,
        data: list[Tuple] = [],
        *,
        title: str | None = "Not specified",
        description: str | None = None,
        separator: int = 5,
        icon_url: str
        | None = "https://lh3.googleusercontent.com/drive-viewer/AITFw-z_IgjwziybK0dE7JNu5i92UEkthC_H89iGhNIiUN_i1cuEnYbi9ijZPBnGRsOGNm465Rzu_GkviBlhjxwAXEp8uNGKxg=w3024-h1514",
        color: Colour | None = Colour(0xADD8E6),
        timeout: float | None = 180,
        auto_defer: bool = True,
    ) -> None:
        super().__init__(timeout=timeout, auto_defer=auto_defer)
        self.data = data
        self.title = title
        self.description = description
        self.separator = separator
        self.icon_url = icon_url
        self.color = color

    @property
    def last_page(self):
        if not self.data:
            return 1
        return ceil(len(self.data) / self.separator)

    @property
    def until_item(self):
        return self.current_page * self.separator

    @property
    def from_item(self):
        return self.until_item - self.separator

    async def send(self, interaction: Interaction):
        self.message = await interaction.send(view=self)
        await self.update_message(self.data[: self.separator])

    def create_embed(self, data):
        embed = (
            Embed(color=self.color, description=self.description)
            .set_author(name=self.title, icon_url=self.icon_url)
            .set_footer(text=f"Page {self.current_page} of {self.last_page}")
        )
        embed.timestamp = datetime.utcnow()

        for name, value in data:
            embed.add_field(name=name, value=value, inline=False)
        return embed

    async def update_message(self, data):
        self.update_buttons()
        await self.message.edit(embed=self.create_embed(data), view=self)

    def update_buttons(self):
        if not self.data:
            self.first_page_button.disabled = True
            self.previous_button.disabled = True
            self.next_button.disabled = True
            self.last_page_button.disabled = True

            self.first_page_button.style = ButtonStyle.gray
            self.previous_button.style = ButtonStyle.gray
            self.next_button.style = ButtonStyle.gray
            self.last_page_button.style = ButtonStyle.gray
        else:
            if self.current_page == 1:
                self.first_page_button.disabled = True
                self.previous_button.disabled = True

                self.first_page_button.style = ButtonStyle.gray
                self.previous_button.style = ButtonStyle.gray
            else:
                self.first_page_button.disabled = False
                self.previous_button.disabled = False

                self.first_page_button.style = ButtonStyle.primary
                self.previous_button.style = ButtonStyle.primary

            if self.current_page == self.last_page:
                self.last_page_button.disabled = True
                self.next_button.disabled = True
                self.last_page_button.style = ButtonStyle.gray
                self.next_button.style = ButtonStyle.gray
            else:
                self.last_page_button.disabled = False
                self.next_button.disabled = False

                self.last_page_button.style = ButtonStyle.primary
                self.next_button.style = ButtonStyle.primary

    @ui.button(emoji="⏪")
    async def first_page_button(self, button: ui.Button, interaction: Interaction):
        await interaction.response.defer()
        self.current_page = 1

        await self.update_message(self.data[: self.until_item])

    @ui.button(emoji="◀️")
    async def previous_button(self, button: ui.Button, interaction: Interaction):
        await interaction.response.defer()
        self.current_page -= 1

        await self.update_message(self.data[self.from_item : self.until_item])

    @ui.button(emoji="▶️")
    async def next_button(self, button: ui.Button, interaction: Interaction):
        await interaction.response.defer()
        self.current_page += 1

        await self.update_message(self.data[self.from_item : self.until_item])

    @ui.button(emoji="⏩")
    async def last_page_button(self, button: ui.Button, interaction: Interaction):
        await interaction.response.defer()
        self.current_page = self.last_page

        await self.update_message(self.data[self.from_item :])
