import datetime
import os

import discord.channel
from discord import app_commands
from discord.ext import tasks, commands
from dotenv import load_dotenv

utc = datetime.timezone.utc

times = [datetime.time(hour=16, tzinfo=utc)]


@app_commands.guild_only()
class TaskCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        load_dotenv()
        self.bot = bot
        self.guild_prime = os.getenv("PRIMARY_GUILD")
        self.guild_test = os.getenv("TEST_GUILD")
        self.batch_update.start()
        self.runTest = "1"
        if self.runTest:
            self.test.start()
        super().__init__()

    def cog_unload(self):
        self.batch_update.cancel()

    @tasks.loop(seconds=1, count=1)
    async def test(self):
        guild = await self.bot.fetch_guild(self.guild_prime)
        channels = await guild.fetch_channels()
        forums = []
        for channel in channels:
            if type(channel) is discord.channel.ForumChannel:
                if channel.name == "trade" or channel.name == "searching-players":
                    forums.append(channel)
        for channel in forums:
            async for thread in channel.archived_threads():
                print(thread)
            for thread in channel.threads:
                print(thread)
        # print("Test message every second.")
        # channel = await self.bot.fetch_channel(1151153113340837941)
        # await channel.send("Test message every two seconds, three times.")

    @tasks.loop(time=times)
    async def batch_update(self):
        guild = ""
        return
