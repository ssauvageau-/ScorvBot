import os

import discord
from discord.ext import commands
from discord.flags import Intents
from dotenv import load_dotenv

from commands.misc import MiscCommandGroup
from commands.moderation import ModerationCommandCog
from commands.announcements import AnnouncementCommandCog
from commands.assign_role import AssignRoleCommandGroup
from commands.tags import TagSystemGroup

load_dotenv()
TEST_GUILD_ID = os.getenv("DISCORD_GUILD")
TEST_GUILD = discord.Object(id=TEST_GUILD_ID)
TOKEN = os.getenv("DISCORD_TOKEN")


class ScorvBot(commands.Bot):
    def __init__(self, intents: Intents, activity: discord.Activity = None) -> None:
        super().__init__(command_prefix="!", intents=intents, activity=activity)

    async def setup_hook(self):
        # Add command cogs here
        await self.add_cog(ModerationCommandCog(self))
        await self.add_cog(AnnouncementCommandCog(self))

        # Add application command groups here
        self.tree.add_command(MiscCommandGroup(self))
        self.tree.add_command(AssignRoleCommandGroup(self))
        self.tree.add_command(TagSystemGroup(self))

        self.tree.copy_global_to(guild=TEST_GUILD)
        await self.tree.sync(guild=TEST_GUILD)


bot_activity = discord.Activity(
    type=discord.ActivityType.watching, name="for fresh meat!"
)
bot = ScorvBot(intents=discord.Intents.all(), activity=bot_activity)


# Global Message Handling
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    elif message.content == "nerd":
        await message.channel.send("nerd")
        await message.delete()
    # elif "https://twitter.com" in message.content:
    #    await message.channel.send(message.content.replace("https://twitter.com", "https://vxtwitter.com"))
    #    await message.delete()
    elif "crab" in message.content:
        await message.add_reaction("🦀")

    await bot.process_commands(message)


bot.run(TOKEN)
