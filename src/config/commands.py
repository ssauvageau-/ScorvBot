import logging
from enum import Enum

import discord
from discord import app_commands, ui
from discord.ext import commands
import redis.asyncio as redis

from .guild_config import GuildConfig


class ConfigFeature(Enum):
    LOG_CHANNEL = "Log Channel"
    MESSAGE_DELETION_LOG = "Message Deletion Log"
    MASKED_URL_LOG = "Masked URL Log"
    TAGS = "Tags"


class LogChannelView(ui.View):
    def __init__(self, redis_client: redis.Redis, guild_config: GuildConfig):
        self.redis_client = redis_client
        self.guild_config = guild_config

        super().__init__(timeout=300)  # 300 seconds. 5 minutes

        self.log_channel_select = ui.ChannelSelect(
            channel_types=[discord.ChannelType.text],
            min_values=1,
            max_values=1,
            default_values=[self.guild_config.log_channel],
            row=0
        )

        self.add_item(self.log_channel_select)

    def _disable_all(self) -> None:
        for item in self.children:
            item.disabled = True

    @ui.button(label="Save", style=discord.ButtonStyle.primary, row=1)
    async def save(self, interaction: discord.Interaction, button: ui.Button):
        self.stop()
        self._disable_all()
        if len(self.log_channel_select.values) == 0:
            # TODO: error
            pass

        self.guild_config.log_channel = self.log_channel_select.values[0]
        await self.guild_config.save_to_redis(self.redis_client)


@app_commands.guild_only()
class ConfigCommandGroup(app_commands.Group, name="config"):
    def __init__(self, bot: commands.Bot, redis_client: redis.Redis):
        self.logger = logging.getLogger("bot")
        self.bot = bot
        self.redis_client = redis_client
        super().__init__()

    @app_commands.command(
        name="view",
        description="View ScorvBot's configuration for this guild",
    )
    @app_commands.checks.has_permissions(manage_guild=True)
    async def view_config(self, interaction: discord.Interaction):
        guild_config = await GuildConfig.from_redis(
            self.redis_client, interaction.guild
        )
        config_embed = guild_config.discord_embed
        config_embed.set_thumbnail(url=self.bot.user.avatar.url)
        await interaction.response.send_message(embed=config_embed)

    @app_commands.command(
        name="edit",
        description="Edit ScorvBot's configuration for this guild",
    )
    @app_commands.describe(feature="The ScorvBot feature to edit")
    @app_commands.checks.has_permissions(manage_guild=True)
    async def edit_config(
        self, interaction: discord.Interaction, feature: ConfigFeature
    ):
        guild_config = await GuildConfig.from_redis(
            self.redis_client, interaction.guild
        )

        match feature:
            case ConfigFeature.LOG_CHANNEL:
                view = LogChannelView(self.redis_client, guild_config)

        await interaction.response.send_message(f"Editing {feature.value} Config", view=view)

    # TODO: uncomment
    # @configure.error
    # async def configure_error(
    #     self, interaction: discord.Interaction, error: app_commands.AppCommandError
    # ):
    #     if isinstance(error, app_commands.errors.MissingPermissions):
    #         await interaction.response.send_message(
    #             "You do not have the required permissions to run this command!",
    #             ephemeral=True,
    #         )
    #     else:
    #         raise error
