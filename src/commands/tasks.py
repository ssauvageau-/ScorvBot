import logging
import json
import os

import discord
from datetime import datetime, time, timezone
from discord import app_commands, NotFound
from discord.ext import tasks, commands
from dotenv import load_dotenv

from utils import load_json_db, dump_json_db

utc = timezone.utc

times = [time(hour=16, tzinfo=utc)]


@app_commands.guild_only()
class TaskCog(commands.Cog, name="Tasks"):
    def __init__(self, bot: commands.Bot):
        load_dotenv()
        self.bot = bot
        self.guild_prime = os.getenv("PRIMARY_GUILD")
        self.guild_test = os.getenv("TEST_GUILD")
        self.env = os.getenv("ENV")
        self.batch_update.start()
        self.runTest = ""
        if self.runTest:
            self.test.start()
        self.thread_expire_days = 21
        self.log_channel_name = "scorv-log"
        self.remove_sundered_role.start()

        super().__init__()

    def cog_unload(self):
        self.batch_update.cancel()
        self.remove_sundered_role.cancel()

    @tasks.loop(seconds=1, count=1)
    async def test(self):
        """
        This will run and get any "old" (by discord's definition) threads, but nothing else.
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
        await self.bot.wait_until_ready()
        if self.env == "prod":
            guild = await self.bot.fetch_guild(self.guild_prime)
        elif self.env == "dev":
            guild = await self.bot.fetch_guild(self.guild_test)

        """
        This will run and get all threads with 'complete' in the title or that are older than 14 days.
        """
        threads = await guild.active_threads()
        currtime = datetime.now(tz=utc)
        closure = []
        for thread in threads:
            diff = currtime - thread.created_at
            diff_s = diff.total_seconds()
            days = divmod(diff_s, 86400)  # 86400 seconds in a day
            if str(self.bot.get_channel(thread.parent_id)) in (
                "searching-players",
                "trade",
            ):
                if (
                    "complete" in thread.name.lower()
                    or days[0] > self.thread_expire_days
                ):
                    closure.append(
                        {
                            "thread": thread,
                            "owner": await self.bot.fetch_user(thread.owner_id),
                            "category": self.bot.get_channel(thread.parent_id),
                        }
                    )
        for thread in closure:
            if "complete" in str(thread["thread"].name.lower()):
                await thread["thread"].delete()
            else:  # not a 'complete' thread - notify user of deletion and invite them to repost if needed
                await thread["owner"].send(
                    f"Hello, {thread['owner'].global_name}, your thread \"{thread['thread'].name}\" in "
                    f"<#{thread['category'].id}> recently expired by exceeding the Grim Dawn server's thread lifespan of"
                    f" {self.thread_expire_days} days. Feel free to repost this thread if you still need its posting. "
                    f'If you no longer needed this thread, please rename future threads to include "complete" in their'
                    f" titles, as those will be more swiftly (and silently) cleaned by ScorvBot. Thank you!"
                )
                await thread["thread"].delete()
        return

    @tasks.loop(minutes=15)
    async def remove_sundered_role(self):
        await self.bot.wait_until_ready()
        if self.env == "prod":
            guild = discord.utils.find(
                lambda guild: str(guild.id) == self.guild_prime, self.bot.guilds
            )
        elif self.env == "dev":
            guild = discord.utils.find(
                lambda guild: str(guild.id) == self.guild_test, self.bot.guilds
            )

        sundered_role = discord.utils.find(
            lambda role: role.name == "Sundered", guild.roles
        )

        if sundered_role is None:
            logging.error("Sundered role not found")
            return

        for member in sundered_role.members:
            await member.remove_roles(sundered_role, reason="Remove Sundered role")
            logging.info(f"Removed Sundered role from {member.display_name}")
