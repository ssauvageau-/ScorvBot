import os

import discord
from discord.ext import commands
from discord.flags import Intents
from dotenv import load_dotenv

from commands.misc import MiscCommandGroup
from commands.moderation import ModerationCommandCog
from commands.assign_role import AssignRoleCommandGroup

load_dotenv()
TEST_GUILD_ID = os.getenv("DISCORD_GUILD")
TEST_GUILD = discord.Object(id=TEST_GUILD_ID)
TOKEN = os.getenv("DISCORD_TOKEN")


class ScorvBot(commands.Bot):
    def __init__(self, intents: Intents, activity: discord.Activity = None) -> None:
        super().__init__(command_prefix="!", intents=intents, activity=activity)

    async def setup_hook(self):
        # Add comand cogs here
        await self.add_cog(ModerationCommandCog(self))

        # Add application command groups here
        self.tree.add_command(MiscCommandGroup(self))
        self.tree.add_command(AssignRoleCommandGroup(self))

        self.tree.copy_global_to(guild=TEST_GUILD)
        await self.tree.sync(guild=TEST_GUILD)


bot_activity = discord.Activity(
    type=discord.ActivityType.watching, name="for fresh meat!"
)
bot = ScorvBot(intents=discord.Intents.all(), activity=bot_activity)
bot.run(TOKEN)
