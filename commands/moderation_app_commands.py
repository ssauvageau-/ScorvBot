from datetime import datetime, timedelta
import json
import os

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

from utils import load_json_db, dump_json_db


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
        self.bot = bot
        super().__init__()

    @app_commands.command(
        name="temp-ban",
        description="Temporarily bans a member for a set number of days",
    )
    @app_commands.describe(member="The member to temporarily ban")
    @app_commands.describe(reason="Reason for the temporary ban")
    @app_commands.describe(duration="The number of whole days to temporarily ban")
    @app_commands.checks.has_any_role("Admin", "Moderator", "Janitor")
    async def temporary_ban_member(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        reason: str,
        duration: int,
    ):
        ban_time = datetime.now()
        ban_expiration = ban_time + timedelta(days=duration)
        temp_ban = {
            "ban_giver": interaction.user.id,  # TODO: rename key
            "recipient_id": member.id,
            "recipient_username": member.name,
            "reason": reason,
            "duration_days": duration,
            "ban_timestamp": ban_time.timestamp,
            "ban_expiration_timestamp": ban_expiration.timestamp,
        }
        self.temp_bans_dict[member.id] = temp_ban
        dump_json_db(self.temp_bans_json_path, self.temp_bans_dict)
        await member.ban(reason=reason)

        # TODO: send DM to user

        # TODO: log ban in channel

    # TODO: background unban & invite task
