import base64
import logging
import os
import json
from typing import List

import discord
from discord import app_commands
from discord.ext import commands
import redis.asyncio as redis
from dotenv import load_dotenv
from enums import redis_keys as rk

REDIS_INVITES = rk.RedisKeys.INVITES.value


class InviteTracker(commands.Cog, name="invites"):
    def __init__(self, bot: commands.Bot, redis_client: redis.Redis):
        load_dotenv()
        self.logger = logging.getLogger("bot")
        self.bot = bot
        self.redis_client = redis_client
        self.log_channel_name = "scorv-log"

    def encode_invite(self, data: str) -> str:
        return base64.b64encode(data.encode("utf-8")).decode("utf-8")

    def decode_invite(self, data: str) -> str:
        return base64.b64decode(data.encode("utf-8")).decode("utf-8")

    # TODO
    def init_invites(self):
        ...

    # TODO
    @commands.Cog.listener(name="on_member_join")
    async def update_invites(self):
        ...

    # TODO
    @commands.Cog.listener(name="on_member_ban")
    async def log_ban(self):
        ...
