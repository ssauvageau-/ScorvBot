from discord import app_commands, Interaction
from discord.ext import commands


@app_commands.guild_only()
class MiscCommandGroup(app_commands.Group, name="misc"):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @app_commands.command(name="test", description="This is a test app command")
    async def test_app_command(self, interaction: Interaction) -> None:
        await interaction.response.send_message("Hello, World!")
