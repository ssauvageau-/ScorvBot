import os

import discord
from discord.ext import commands
from discord.flags import Intents
from dotenv import load_dotenv

from commands.moderation import ModerationCommandCog
from commands.announcements import AnnouncementCommandGroup
from commands.assign_role import AssignRoleCommandGroup
from commands.graph_roles import GraphRoleCommandGroup
from commands.tags import TagSystemGroup
from commands.misc import MiscCommandCog
from commands.raffle import RaffleCommandGroup
from commands.tasks import TaskCog
from events import Events

load_dotenv()
TEST_GUILD_ID = os.getenv("TEST_GUILD")
TEST_GUILD = discord.Object(id=TEST_GUILD_ID)
PRIMARY_GUILD_ID = os.getenv("PRIMARY_GUILD")
PRIMARY_GUILD = discord.Object(id=PRIMARY_GUILD_ID)
TOKEN = os.getenv("DISCORD_TOKEN")


class ScorvBot(commands.Bot):
    def __init__(self, intents: Intents, activity: discord.Activity = None) -> None:
        super().__init__(command_prefix="!", intents=intents, activity=activity)

    async def setup_hook(self):
        # Add command cogs here
        await self.add_cog(Events(self))
        await self.add_cog(ModerationCommandCog(self))
        await self.add_cog(MiscCommandCog(self))
        await self.add_cog(TaskCog(self))

        # Add application command groups here
        self.tree.add_command(AnnouncementCommandGroup(self))
        self.tree.add_command(AssignRoleCommandGroup(self))
        self.tree.add_command(TagSystemGroup(self))
        self.tree.add_command(GraphRoleCommandGroup(self))
        self.tree.add_command(RaffleCommandGroup(self))

        self.tree.copy_global_to(guild=TEST_GUILD)
        await self.tree.sync(guild=TEST_GUILD)
        # self.tree.copy_global_to(guild=PRIMARY_GUILD)
        # await self.tree.sync(guild=PRIMARY_GUILD)


bot_activity = discord.Activity(
    type=discord.ActivityType.watching, name="for fresh meat!"
)
bot = ScorvBot(intents=discord.Intents.all(), activity=bot_activity)
bot.run(TOKEN)
