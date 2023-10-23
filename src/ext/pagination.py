from datetime import datetime
from math import ceil

from nextcord import ButtonStyle, Colour, Embed, Interaction, ui


class PaginationView(ui.View):
    current_page: int = 1

    def __init__(
        self,
        data: list[tuple[str, str] | dict[str, str]],
        *,
        title: str | None = "Not specified",
        description: str | None = None,
        separator: int = 5,
        icon_url: str | None = None,
        color: Colour | None = Colour(0xADD8E6),
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
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
            Embed(color=self.color, description=self.description, timestamp=datetime.utcnow())
            .set_author(name=self.title, icon_url=self.icon_url)
            .set_footer(text=f"Page {self.current_page} of {self.last_page}")
        )

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
