import os

import discord
import redis.asyncio as redis
from discord.ext import commands
from discord.flags import Intents
from dotenv import load_dotenv

from logging_config import setup_logging
from commands.announcements import AnnouncementCommandGroup
from commands.assign_role import AssignRoleCommandGroup
from commands.graph_roles import GraphRoleCommandGroup
from commands.tags import TagSystemGroup
from commands.misc import MiscCommandCog
from commands.raffle import RaffleCommandGroup
from commands.tasks import TaskCog
from commands.moderation import ModerationCommandGroup
from events import Events

load_dotenv()
TEST_GUILD_ID = os.getenv("TEST_GUILD")
TEST_GUILD = discord.Object(id=TEST_GUILD_ID)
PRIMARY_GUILD_ID = os.getenv("PRIMARY_GUILD")
PRIMARY_GUILD = discord.Object(id=PRIMARY_GUILD_ID)
TOKEN = os.getenv("DISCORD_TOKEN")
ENV = os.getenv("ENV")
REDIS_HOST_NAME = os.getenv("REDIS_HOST_NAME", "redis")
REDIS_HOST_PORT = os.getenv("REDIS_HOST_PORT", "6379")


class ScorvBot(commands.Bot):
    def __init__(self, intents: Intents, activity: discord.Activity = None) -> None:
        super().__init__(command_prefix="!", intents=intents, activity=activity)

    async def setup_hook(self):
        redis_client = redis.Redis(
            host=REDIS_HOST_NAME, port=REDIS_HOST_PORT, decode_responses=True
        )
        try:
            await redis_client.ping()
        except Exception as e:
            print("Could not connect to Redis:", e)
            exit(1)

        # Add command cogs here
        await self.add_cog(Events(self))
        await self.add_cog(MiscCommandCog(self, redis_client))
        await self.add_cog(TaskCog(self))

        # Add application command groups here
        self.tree.add_command(AnnouncementCommandGroup(self))
        self.tree.add_command(AssignRoleCommandGroup(self))
        self.tree.add_command(TagSystemGroup(self, redis_client))
        self.tree.add_command(GraphRoleCommandGroup(self))
        self.tree.add_command(RaffleCommandGroup(self, redis_client))
        self.tree.add_command(ModerationCommandGroup(self))

        if ENV == "dev":
            self.tree.copy_global_to(guild=TEST_GUILD)
            await self.tree.sync(guild=TEST_GUILD)
        elif ENV == "prod":
            self.tree.copy_global_to(guild=PRIMARY_GUILD)
            await self.tree.sync(guild=PRIMARY_GUILD)


logging_handler = setup_logging()

bot_activity = discord.Activity(
    type=discord.ActivityType.watching, name="for fresh meat!"
)
bot = ScorvBot(intents=discord.Intents.all(), activity=bot_activity)

# Run bot. Suppress default logging config since we used our own
bot.run(TOKEN, log_handler=None)
