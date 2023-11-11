from datetime import datetime, timedelta, timezone
import json
import os
from typing import Dict

import discord
from discord import app_commands, TextStyle
from discord.ext import commands
from dotenv import load_dotenv

from utils import load_json_db, dump_json_db

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


@app_commands.guild_only()
class ModerationCommandGroup(app_commands.Group, name="moderation"):
    def __init__(self, bot: commands.Bot):
        load_dotenv()
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
        super().__init__()

    @app_commands.command(
        name="temp-ban",
        description="Temporarily bans a member for a set number of days",
    )
    @app_commands.describe(member="The member to temporarily ban")
    @app_commands.checks.has_any_role(*COMMAND_ROLE_ALLOW_LIST)
    async def temporary_ban_member_modal(
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
            async for message in interaction.channel.history(limit=deletion):
                await message.delete()

        await interaction.followup.send(f"Deleted {number} messages", ephemeral=True)
