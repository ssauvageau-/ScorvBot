import logging

import discord
from discord.ext import commands
import redis.asyncio as redis

from .guild_config import GuildConfig


class ConfigEventsCog(commands.Cog, name="Config Events"):
    def __init__(self, bot: commands.Bot, redis_client: redis.Redis):
        self.logger = logging.getLogger("bot")
        self.bot = bot
        self.redis_client = redis_client
        super().__init__()

    @commands.Cog.listener("on_guild_join")
    async def create_config_on_guild_join(self, guild: discord.Guild) -> None:
        """
        Initialize guild config with default (valid) values when a guild is joined
        """
        log_info = {
            "guild_id": guild.id,
            "guild_name": guild.name,
            "guild_owner": guild.owner.name,
        }

        default_log_channel = (
            guild.public_updates_channel
            or guild.system_channel
            or guild.text_channels[0]
        )

        if default_log_channel is None:
            self.logger.error(
                "Failed to initialize new guild config. No text channel found %s",
                log_info,
            )
            return

        guild_config = GuildConfig(guild, default_log_channel)
        result = await guild_config.save_to_redis()

        if result:
            self.logger.info("Initialized new guild config %s", log_info)
        else:
            log_info["guild_config"] = guild_config.__dict__
            self.logger.error("Failed to initialize new guild config %s", log_info)
            owner_dm_channel = await guild.owner.create_dm()
            await owner_dm_channel.send(
                f"There was a problem creating a configuration for your guild '{guild.name}'."
                + "\n\nScorvBot will not function properly without a configuration. Please use the `/configure` command within your guild to create one."
            )

    @commands.Cog.listener("on_guild_remove")
    async def delete_config_on_guild_remove(self, guild: discord.Guild) -> None:
        """
        Remove a guild config from Redis when the bot leaves a guild
        """
        result = await self.redis_client.delete(GuildConfig._redis_key(guild.id))
        if result:
            self.logger.info("Deleted guild config %s", {"guild_id": guild.id})
