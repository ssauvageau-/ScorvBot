import base64
import logging
import os
import json
import typing
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
        self.env = os.getenv("ENV")
        self.guild_id = (
            os.getenv("PRIMARY_GUILD")
            if self.env == "prod"
            else os.getenv("TEST_GUILD")
        )
        self.redis_client = redis_client
        self.log_channel_name = "scorv-log"

    async def init_invites(self):
        gld = discord.utils.find(
            lambda guild: str(guild.id) == self.guild_id, self.bot.guilds
        )
        invs = await gld.invites()
        prior_load = await self.redis_client.hgetall(name=REDIS_INVITES)

        for inv in invs:
            sid = str(inv.id)
            if sid in prior_load:
                jval = json.loads(prior_load[sid])
                if inv.uses == jval[0]:
                    continue
                await self.redis_client.hset(
                    name=REDIS_INVITES, key=sid, value=json.dumps(jval)
                )
            else:
                await self.redis_client.hset(
                    name=REDIS_INVITES, key=sid, value=json.dumps([inv.uses, []])
                )
                # [number of times invite was used, tracked users who used the invite]

    @commands.Cog.listener(name="on_member_join")
    async def update_invites(self, member: discord.Member):
        gld = discord.utils.find(
            lambda guild: str(guild.id) == self.guild_id, self.bot.guilds
        )
        post_join_invs = await gld.invites()
        pre_join_invs = self.redis_client.hgetall(name=REDIS_INVITES)
        if not pre_join_invs:
            await self.init_invites()
            return
        for inv, values in pre_join_invs.items():
            # list comprehension to make code concise, should only be one item ([0])
            hits = [x for x in post_join_invs if str(x.id) == inv]
            jval = json.loads(values)
            if hits and hits[0].uses > jval[0]:
                users = jval[1].append(member.id)
                await self.redis_client.hset(
                    name=REDIS_INVITES,
                    key=str(hits[0].id),
                    value=json.dumps([jval[0] + 1, users]),
                )
                self.logger.info(f"Added {member.id} to Invite Roster of Invite {inv}")

    @commands.Cog.listener(name="on_invite_create")
    async def new_invite(self, invite: discord.Invite):
        await self.redis_client.hset(
            name=REDIS_INVITES, key=invite.id, value=json.dumps([0, []])
        )
        self.logger.info(f"Added new Invite: {invite.id}")

    @commands.Cog.listen(name="on_invite_deleted")
    async def del_invite(self, invite: discord.Invite):
        await self.redis_client.delete(str(invite.id))
        self.logger.info(f"Deleted Invite: {invite.id}")

    # TODO
    @commands.Cog.listener(name="on_member_ban")
    async def log_ban(self):
        ...
