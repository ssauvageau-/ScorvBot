from typing import Any, Dict

import discord
import redis.asyncio as redis

from enums import RedisKeys


class GuildConfig:
    def __init__(
        self,
        guild: discord.Guild,
        log_channel: discord.TextChannel,
        message_deletion_log_channel: discord.TextChannel = None,
        masked_url_log_channel: discord.TextChannel = None,
        tag_approval_channel: discord.TextChannel = None,
    ):
        self.guild = guild
        self.log_channel = log_channel
        self.message_deletion_log_channel = message_deletion_log_channel or log_channel
        self.masked_url_log_channel = masked_url_log_channel or log_channel
        self.tag_approval_channel = tag_approval_channel or log_channel

    @property
    def redis_mapping(self) -> Dict[str, Any]:
        """
        A mapping for the key/value pairs stored in Redis
        """
        return {
            "guild_id": self.guild.id,
            "log_channel_id": self.log_channel.id,
            "message_deletion_log_channel_id": self.message_deletion_log_channel.id,
            "masked_url_log_channel_id": self.masked_url_log_channel.id,
            "tag_approval_channel_id": self.tag_approval_channel.id,
        }

    @property
    def discord_embed(self) -> discord.Embed:
        """
        A Discord Embed from the saved configuration
        """
        embed = discord.Embed(
            title="ScorvBot Configuration",
        )
        embed.add_field(
            name="Log Channel", value=self.log_channel.mention, inline=False
        )
        embed.add_field(
            name="Message Deletion Log Channel",
            value=self.message_deletion_log_channel.mention,
            inline=False,
        )
        embed.add_field(
            name="Masked URL Log Channel",
            value=self.masked_url_log_channel.mention,
            inline=False,
        )
        embed.add_field(
            name="Tag Approval Channel",
            value=self.tag_approval_channel.mention,
            inline=False,
        )
        embed.set_author(name=self.guild.name, icon_url=self.guild.icon.url)
        return embed

    @staticmethod
    def _redis_key(guild_id: int = None) -> str:
        return f"{RedisKeys.GUILD_CONFIG.value}:{guild_id}"

    @classmethod
    async def from_redis(
        cls,
        redis_client: redis.Redis,
        guild: discord.Guild,
    ):
        """
        Get an instance of the GuildConfig class with values from Redis
        """
        id_guild_config = await redis_client.hgetall(
            name=cls._redis_key(guild_id=guild.id)
        )

        log_channel_id = id_guild_config["log_channel_id"]
        log_channel = guild.get_channel(int(log_channel_id))
        if log_channel is None:
            raise Exception(
                "Log channel not found",
                "guild_id",
                guild.id,
                "log_channel_id",
                log_channel_id,
            )

        message_deletion_log_channel_id = id_guild_config[
            "message_deletion_log_channel_id"
        ]
        message_deletion_log_channel = (
            log_channel
            if message_deletion_log_channel_id == log_channel_id
            else guild.get_channel(int(message_deletion_log_channel_id))
        )
        if message_deletion_log_channel is None:
            raise Exception(
                "Message deletion log channel not found in guild",
                "guild_id",
                guild.id,
                "message_deletion_channel_id",
                message_deletion_log_channel_id,
            )

        masked_url_log_channel_id = id_guild_config["masked_url_log_channel_id"]
        masked_url_log_channel = (
            log_channel
            if masked_url_log_channel_id == log_channel_id
            else guild.get_channel(int(masked_url_log_channel_id))
        )
        if masked_url_log_channel is None:
            raise Exception(
                "Masked url log channel not found in guild",
                "guild_id",
                guild.id,
                "masked_url_log_channel_id",
                masked_url_log_channel_id,
            )

        tag_approval_channel_id = id_guild_config["tag_approval_channel_id"]
        tag_approval_channel = (
            log_channel
            if tag_approval_channel_id == log_channel_id
            else guild.get_channel(int(tag_approval_channel_id))
        )
        if tag_approval_channel is None:
            raise Exception(
                "Tag approval channel not found in guild",
                "guild_id",
                guild.id,
                "tag_approval_channel_id",
                tag_approval_channel_id,
            )

        return cls(
            guild,
            log_channel,
            message_deletion_log_channel,
            masked_url_log_channel,
            tag_approval_channel,
        )

    async def save_to_redis(self, redis_client: redis.Redis) -> int:
        """
        Save this instance of the GuildConfig class to Redis.

        Returns the amount of keys changed. This will return 0 if no values are updated
        """
        return await redis_client.hset(
            name=self._redis_key(self.guild.id), mapping=self.redis_mapping
        )
