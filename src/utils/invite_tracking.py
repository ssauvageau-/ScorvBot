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
        self.gld = discord.utils.find(
            lambda guild: str(guild.id) == self.guild_id, self.bot.guilds
        )

    async def init_invites(self, invs):
        prior_load = await self.redis_client.hgetall(name=REDIS_INVITES)

        for inv in invs:
            sid = inv.code
            if sid in prior_load:
                jval = json.loads(prior_load[sid])
                if inv.uses == jval[0]:
                    continue
                await self.redis_client.hset(
                    name=REDIS_INVITES, key=sid, value=json.dumps(jval)
                )
            else:
                inviter_id = inv.inviter.id if inv.inviter else 0
                await self.redis_client.hset(
                    name=REDIS_INVITES,
                    key=sid,
                    value=json.dumps([inv.uses, [], inviter_id])
                    # [number of times invite was used, tracked users who used the invite, ID of invite creator]
                )

    @commands.Cog.listener(name="on_member_join")
    async def update_invites(self, member: discord.Member):
        post_join_invs = await self.gld.invites()
        pre_join_invs = await self.redis_client.hgetall(name=REDIS_INVITES)
        if not pre_join_invs:
            await self.init_invites(post_join_invs)
            return
        for inv, values in pre_join_invs.items():
            # list comprehension to make code concise, should only be one item ([0])
            hits = [x for x in post_join_invs if x.code == inv]
            jvals = json.loads(values)
            if hits and hits[0].uses > jvals[0]:
                users = jvals[1].append(member.id)
                await self.redis_client.hset(
                    name=REDIS_INVITES,
                    key=hits[0].code,
                    value=json.dumps([jvals[0] + 1, users, jvals[2]]),
                )
                self.logger.info(f"Added {member.id} to Invite Roster of Invite {inv}")

    @commands.Cog.listener(name="on_invite_create")
    async def new_invite(self, invite: discord.Invite):
        inviter_id = invite.inviter.id if invite.inviter else 0
        await self.redis_client.hset(
            name=REDIS_INVITES, key=invite.code, value=json.dumps([0, [], inviter_id])
        )
        self.logger.info(f"Added new Invite: {invite.code}")

    @commands.Cog.listener(name="on_invite_deleted")
    async def del_invite(self, invite: discord.Invite):
        await self.redis_client.delete(invite.code)
        self.logger.info(f"Deleted Invite: {invite.code}")

    @commands.Cog.listener(name="on_member_ban")
    async def log_ban(self, member: discord.Member):
        log_channel = discord.utils.find(
            lambda channel: channel.name == self.log_channel_name,
            self.gld.channels,
        )
        if log_channel is None:
            raise Exception("Log channel not found")
        invites = await self.redis_client.hgetall(name=REDIS_INVITES)
        use_exception_limit = 150  # ignore invites that reach this limit; ultra-popular ones are well-established
        caught_invites = []
        for code, values in invites:
            jvals = json.loads(values)
            if member.id in jvals[1]:
                if jvals[0] >= use_exception_limit:
                    return
                if jvals[2] == 0:
                    # no data to be gleamed :( - likely an older invite/Server Discovery, both of which are fine.
                    return
                caught_invites.append([code, jvals[2]])
        embed = discord.Embed(
            color=discord.Color.red(),
            title=f"{member.name} has been banned!",
            description=f"{member.global_name}",
        )
        embed.set_author(name=member.display_name, icon_url=member.display_avatar.url)
        for i in range(len(caught_invites)):
            embed.add_field(name="Used Invite", value=caught_invites[i][0], inline=True)
            embed.add_field(
                name="Invite Creator", value=caught_invites[i][1], inline=True
            )
            if i < len(caught_invites) - 1:
                embed.add_field(name="\u200B", value="\u200B")  # newline
        await log_channel.send(embed=embed)
