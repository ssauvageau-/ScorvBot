import os

import discord
from discord.flags import Intents
from dotenv import load_dotenv

from commands.app_commands import MiscCommandGroup

load_dotenv()
TEST_GUILD_ID = os.getenv("DISCORD_GUILD")
TEST_GUILD = discord.Object(id=TEST_GUILD_ID)
TOKEN = os.getenv("DISCORD_TOKEN")


class ScorvClient(discord.Client):
    def __init__(self, intents: Intents) -> None:
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.add_command(MiscCommandGroup())
        self.tree.copy_global_to(guild=TEST_GUILD)
        await self.tree.sync(guild=TEST_GUILD)


client = ScorvClient(intents=discord.Intents.default())
client.run(TOKEN)
