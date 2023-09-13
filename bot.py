import os

import discord
from discord.flags import Intents
from dotenv import load_dotenv

from commands.app_commands import MiscCommandGroup
from cogs.moderation import ModerationCommandCog

load_dotenv()
TEST_GUILD_ID = os.getenv("DISCORD_GUILD")
TEST_GUILD = discord.Object(id=TEST_GUILD_ID)
TOKEN = os.getenv("DISCORD_TOKEN")


class ScorvClient(discord.Client):
    def __init__(self, intents: Intents) -> None:
        activity = discord.Activity(type=discord.ActivityType.watching, name="for fresh meat!")
        super().__init__(command_prefix="!", intents=intents, activity=activity)
        self.tree = discord.app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.add_command(MiscCommandGroup())
#        self.tree.add_command(ModerationCommandCog()) # expects a 'bot'
        self.tree.copy_global_to(guild=TEST_GUILD)
        await self.tree.sync(guild=TEST_GUILD)


client = ScorvClient(intents=discord.Intents.default())
#client.load_extension("cogs.moderation")
client.run(TOKEN)
