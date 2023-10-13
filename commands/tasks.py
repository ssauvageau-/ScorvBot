import os

import discord
import datetime
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
        await self.bot.wait_until_ready()
        guild = await self.bot.fetch_guild(self.guild_prime)

        """
        This will run and get all threads with 'complete' in the title or that are older than 14 days.
        """
        # threads = await guild.active_threads()
        # currtime = datetime.datetime.now(tz=utc)
        # for thread in threads:
        #     diff = currtime - thread.created_at
        #     diff_s = diff.total_seconds()
        #     days = divmod(diff_s, 86400)  # 86400 seconds in a day
        #     if "complete" in thread.name.lower() or days[0] > 14:
        #         print(thread, await self.bot.fetch_user(thread.owner_id))

        """
        This will run and get any "old" (by discord's definition) threads.
        """
        # channels = await guild.fetch_channels()
        # forums = []
        # for channel in channels:
        #     if type(channel) is discord.channel.ForumChannel:
        #         if channel.name == "trade" or channel.name == "searching-players":
        #             forums.append(channel)
        # for channel in forums:
        #     async for thread in channel.archived_threads():
        #         print(thread)  # works
        #     for thread in channel.threads:
        #         print(thread)  # doesn't work, channel properties not cached by runtime?

    @tasks.loop(time=times)
    async def batch_update(self):
        guild = ""
        return
