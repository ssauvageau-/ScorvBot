from discord import app_commands, Interaction


@app_commands.guild_only()
class MiscCommandGroup(app_commands.Group):
    @app_commands.command(name="test", description="This is a test app command")
    async def test_app_command(self, interaction: Interaction) -> None:
        await interaction.response.send_message("Hello, World!")
