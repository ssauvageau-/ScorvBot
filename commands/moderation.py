import asyncio

import aiohttp
from datetime import datetime, timedelta, timezone
import json
import logging
import os
from typing import Dict

import discord
from discord import app_commands, http, TextStyle
from discord.ext import commands
from dotenv import load_dotenv
import requests

from utils import load_json_db, dump_json_db, log_utils

COMMAND_ROLE_ALLOW_LIST = ["Admin", "Moderator", "Janitor"]


class TemporaryBanModal(discord.ui.Modal):
    duration = discord.ui.TextInput(
        label="Duration in Days", default="1", required=True
    )
    reason = discord.ui.TextInput(
        label="Reason",
        style=TextStyle.paragraph,
        placeholder="Reason for the temporary ban",
        required=True,
    )

    def __init__(
        self,
        member: discord.Member,
        log_channel_name: str,
        json_path: str,
        temp_bans: Dict[str, Dict],
    ):
        super().__init__(title=f"Temporarily ban {member.display_name}")
        self.member = member
        self.log_channel_name = log_channel_name
        self.json_path = json_path
        self.temp_bans = temp_bans

    async def on_submit(self, interaction: discord.Interaction):
        try:
            duration_days = int(self.duration.value)
        except ValueError:
            await interaction.response.send_message(
                "Field 'Duration in Days' must be a number, i.e. `5`", ephemeral=True
            )
            return

        ban_time = datetime.utcnow()
        ban_expiration = ban_time + timedelta(days=duration_days)
        temp_ban = {
            "ban_giver_id": interaction.user.id,
            "ban_giver_username": interaction.user.name,
            "recipient_id": self.member.id,
            "recipient_username": self.member.name,
            "recipient_roles": [role.name for role in self.member.roles],
            "reason": self.reason.value,
            "duration_days": duration_days,
            "ban_timestamp": ban_time.timestamp(),
            "ban_expiration_timestamp": ban_expiration.timestamp(),
        }
        self.temp_bans[str(self.member.id)] = temp_ban
        dump_json_db(self.json_path, self.temp_bans)

        dm_embed = discord.Embed(
            color=discord.Color.red(),
            title="Temporarily Banned",
            description=f"You have been banned from **{interaction.guild.name}** for **{duration_days} day(s)**. You will be notified when your ban expires if you allow messages from non-mutual server members.",
            timestamp=ban_time,
        )
        dm_embed.set_thumbnail(url=interaction.guild.icon.url)
        dm_embed.add_field(
            name="Expiration date", value=f"<t:{int(ban_expiration.timestamp())}:f>"
        )
        dm_embed.add_field(name="Reason for ban", value=self.reason.value)

        await self.member.send(embed=dm_embed)
        await self.member.ban(reason=self.reason.value)

        log_channel = discord.utils.find(
            lambda c: c.name == self.log_channel_name, interaction.guild.channels
        )
        if log_channel is not None:
            log_embed = discord.Embed(
                color=discord.Color.red(), title="Temporary Ban", timestamp=ban_time
            )
            log_embed.set_author(
                name=interaction.user.display_name,
                icon_url=interaction.user.display_avatar,
            )
            log_embed.set_thumbnail(url=self.member.display_avatar)
            log_embed.add_field(name="Member", value=self.member.mention, inline=True)
            log_embed.add_field(
                name="Duration", value=f"{duration_days} day(s)", inline=True
            )
            log_embed.add_field(
                name="Expiration date",
                value=f"<t:{int(ban_expiration.timestamp())}:f>",
                inline=True,
            )
            log_embed.add_field(name="Reason for ban", value=self.reason.value)

            await log_channel.send(embed=log_embed)

        await interaction.response.send_message(
            f"Temporarily banned **{self.member.display_name}** for **{duration_days} day(s)**",
            ephemeral=True,
        )


SPY_BOTS = "https://gist.githubusercontent.com/Dziurwa14/05db50c66e4dcc67d129838e1b9d739a/raw/b0c0ebba557521e9234074a22e544ab48f448f6a/spy.pet%20accounts"


@app_commands.guild_only()
class ModerationCommandGroup(app_commands.Group, name="moderation"):
    def __init__(self, bot: commands.Bot):
        load_dotenv()
        self.logger = logging.getLogger("bot")
        self.temp_bans_json_path = os.getenv("TEMP_BANS_JSON_PATH")
        try:
            self.temp_bans_dict = load_json_db(self.temp_bans_json_path)
        except json.decoder.JSONDecodeError:
            self.temp_bans_dict = {}
        except FileNotFoundError:
            self.temp_bans_dict = {}
            if not os.path.exists("json"):
                os.makedirs("json")
            os.close(os.open(self.temp_bans_json_path, os.O_CREAT))
        self.log_channel_name = "scorv-log"
        self.bot = bot
        self.spy_bots = requests.get(SPY_BOTS).json()
        self._session = None  # filled in `reload_spy_bots` function so we don't get DeprecationWarning
        super().__init__()

    @commands.command(name="reload-spy-bots")
    @commands.has_any_role(*COMMAND_ROLE_ALLOW_LIST)
    async def reload_spy_bots(self, ctx: commands.Context):
        if self._session is None:
            self._session = aiohttp.ClientSession()
        response = await self._session.get(SPY_BOTS)
        self.spy_bots = await response.json()
        await ctx.message.add_reaction("\N{OK HAND SIGN}")

    @app_commands.command(
        name="spy-ban",
        description="Ban spy.pet accounts identified by @PirateSoftware.",
    )
    @app_commands.checks.has_any_role(*COMMAND_ROLE_ALLOW_LIST)
    async def ban_spy_pet(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True, thinking=True)
        guild_id = interaction.guild_id
        await self.bot.http.request(
            http.Route("POST", "/guilds/{guild_id}/bulk-ban", guild_id=guild_id),
            json={"user_ids": self.spy_bots},
            reason="spy.pet bot",
        )
        await interaction.followup.send("Banned spy.pet accounts.")

    @app_commands.command(
        name="temp-ban",
        description="Temporarily bans a member for a set number of days",
    )
    @app_commands.describe(member="The member to temporarily ban")
    @app_commands.checks.has_any_role(*COMMAND_ROLE_ALLOW_LIST)
    async def temporary_ban_member(
        self, interaction: discord.Interaction, member: discord.Member
    ):
        await interaction.response.send_modal(
            TemporaryBanModal(
                member=member,
                log_channel_name=self.log_channel_name,
                json_path=self.temp_bans_json_path,
                temp_bans=self.temp_bans_dict,
            )
        )

    @app_commands.command(
        name="clear-messages",
        description="Delete a number of recent messages in the channel",
    )
    @app_commands.describe(number="The number of recent messages to delete")
    @app_commands.checks.has_any_role(*COMMAND_ROLE_ALLOW_LIST)
    async def clear(self, interaction: discord.Interaction, number: int):
        await interaction.response.defer(ephemeral=True, thinking=True)

        if number > 5:
            deletions = [5 for _ in range(0, int(number / 5))]
            if number % 5 > 0:
                deletions.append(number % 5)
        else:
            deletions = [number]

        for deletion in deletions:
            await interaction.channel.purge(limit=deletion)

        await interaction.followup.send(f"Deleted {number} messages", ephemeral=True)

    @app_commands.command(
        name="range-delete",
        description="Delete all messages in a channel that occur between two supplied messages, inclusive.",
    )
    @app_commands.describe(
        msg_one="ID of the first of the two message block limits, inclusive.",
        msg_two="ID of the second of the two message block limits, inclusive.",
    )
    @app_commands.checks.has_any_role(*COMMAND_ROLE_ALLOW_LIST)
    async def range_delete(
        self,
        interaction: discord.Interaction,
        msg_one: str,
        msg_two: str,
        limit: int = 200,
    ):
        chan = interaction.channel
        m1 = await chan.fetch_message(int(msg_one))
        m2 = await chan.fetch_message(int(msg_two))
        if m1 is None or m2 is None:
            await interaction.response.send_message(
                "Messages not found in calling channel, terminating operation.\nYou must use this command from the channel that contains both messages.",
                ephemeral=True,
            )
        await interaction.response.defer(ephemeral=True, thinking=True)
        hist = [message async for message in chan.history(limit=limit)]
        print(hist)
        bound1, bound2 = 0, 0
        for x in range(len(hist)):
            if hist[x].id == int(msg_one):
                bound1 = x
            elif hist[x].id == int(msg_two):
                bound2 = x
        if bound1 == 0 or bound2 == 0:
            await interaction.followup.send(
                f"Messages not found within history of {limit} messages in channel.",
                ephemeral=True,
            )
        # python list slicing is [x:y) by default, need to add 1 to upper bound
        deletions = (
            hist[bound1 : bound2 + 1] if bound1 < bound2 else hist[bound2 : bound1 + 1]
        )
        queue = [deletions[i : i + 5] for i in range(0, len(deletions), 5)]
        for batch in queue:
            for msg in batch:
                await msg.delete()
            await asyncio.sleep(1)
        await interaction.followup.send(
            f"Deleted {len(deletions)} messages.", ephemeral=True
        )

    @temporary_ban_member.error
    @clear.error
    async def missing_role_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ):
        if isinstance(error, app_commands.errors.MissingAnyRole):
            await interaction.response.send_message(
                "You do not have the required permissions to use this command!",
                ephemeral=True,
            )
            self.logger.info(
                f"User {log_utils.format_user(interaction.user)} attempted to use command {log_utils.format_app_command_name(interaction.command)} without proper permissions"
            )
        else:
            raise error
