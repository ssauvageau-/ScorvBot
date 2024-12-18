import base64
import os
import json
from typing import List

import discord
import redis.asyncio as redis
from discord.ui import Button
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

from enums import redis_keys as rk


REDIS_TAGS_KEY_NAME = rk.RedisKeys.TAGS.value


@app_commands.guild_only()
class TagSystemGroup(app_commands.Group, name="tag"):
    def __init__(self, bot: commands.Bot, redis_client: redis.Redis):
        load_dotenv()
        self.approval_channel = os.getenv("TAG_APPROVAL_ID")
        self.bot = bot
        self.redis_client = redis_client
        super().__init__()

    def encode_tag_data(self, data: str) -> str:
        return base64.b64encode(data.encode("utf-8")).decode("utf-8")

    def decode_tag_data(self, data: str) -> str:
        return base64.b64decode(data.encode("utf-8")).decode("utf-8")

    async def tag_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> List[app_commands.Choice[str]]:
        choices = await self.redis_client.hkeys(REDIS_TAGS_KEY_NAME)
        tags = [
            app_commands.Choice(name=choice, value=choice)
            for choice in choices
            if current.lower() in choice.lower()
        ]
        if len(tags) > 25:
            return tags[:25]
            # Discord autocomplete only supports 25 elements
            # Without this, users are not shown any elements of the tag list when total tags > 25
        return tags

    @app_commands.command(name="post", description="Post a tag in chat.")
    @app_commands.autocomplete(choice=tag_autocomplete)
    async def post_tag(self, interaction: discord.Interaction, choice: str):
        raw_tag = await self.redis_client.hget(name=REDIS_TAGS_KEY_NAME, key=choice)
        tag = json.loads(raw_tag)
        decoded_data = self.decode_tag_data(tag["data"])
        await interaction.response.send_message(decoded_data)

    @app_commands.command(name="submit", description="Submit a new tag for review.")
    async def submit_tag(
        self, interaction: discord.Interaction, tag: str, content: str
    ):
        tag_clean = tag.strip()
        content_clean = content.strip()
        if await self.redis_client.hexists(REDIS_TAGS_KEY_NAME, tag_clean):
            await interaction.response.send_message(
                f"Tag `{tag_clean}` already exists!", ephemeral=True
            )
            return
        else:  # redundant but indented for clarity
            await self.bot.get_channel(int(self.approval_channel)).send(
                embed=self.create_embed(interaction, tag_clean, content_clean),
                view=await self.create_approval_buttons(
                    interaction, tag_clean, content_clean
                ),
            )
            await interaction.response.send_message(
                f"Tag `{tag_clean}` has been submitted for review.", ephemeral=True
            )
            return

    @app_commands.command(name="remove", description="Remove a tag")
    @app_commands.autocomplete(tag=tag_autocomplete)
    @app_commands.checks.has_any_role("Admin", "Moderator", "Janitor")
    async def remove_tag(self, interaction: discord.Interaction, tag: str):
        # TODO - Extract deletion to confirmation dialog buttons?
        tag_clean = tag.strip()
        if await self.redis_client.hexists(REDIS_TAGS_KEY_NAME, tag_clean):
            await self.redis_client.hdel(REDIS_TAGS_KEY_NAME, tag_clean)
            await interaction.response.send_message(
                "Tag successfully removed.", ephemeral=True
            )

    @remove_tag.error
    async def remove_tag_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ):
        if isinstance(error, app_commands.errors.MissingAnyRole):
            await interaction.response.send_message(
                "You do not have the required permissions to run this command!",
                ephemeral=True,
            )
        else:
            raise error

    async def create_approval_buttons(
        self, submission: discord.Interaction, tag_name: str, data: str
    ):
        buttons = discord.ui.View(timeout=None)
        approval_button = Button(
            style=discord.ButtonStyle.green,
            label="Approve",
            custom_id="approve_button",
            disabled=False,
            emoji="👍",
            row=1,
        )

        async def approval_callback(interaction: discord.Interaction):
            # We don't use this Interaction but Discord *will* send it into our override, so we need to catch it
            await submission.user.send(
                f"Your tag: `{tag_name}` has been approved on the Grim Dawn server!"
            )
            await interaction.message.channel.send(
                f"Tag `{tag_name}` approved by {interaction.user}."
            )
            encoded_data = self.encode_tag_data(data)
            tag = {
                "data": encoded_data,
                "author": interaction.user.name,
                "creation": interaction.created_at.strftime("%a %d %b %Y, %I:%M%p %Z"),
            }
            await self.redis_client.hset(
                name=REDIS_TAGS_KEY_NAME, key=tag_name, value=json.dumps(tag)
            )
            await interaction.message.delete()

        approval_button.callback = approval_callback

        deny_button = Button(
            style=discord.ButtonStyle.red,
            label="Deny",
            custom_id="deny_button",
            disabled=False,
            emoji="👎",
            row=1,
        )

        async def deny_callback(interaction: discord.Interaction):
            # We don't use this Interaction but Discord *will* send it into our override, so we need to catch it
            await submission.user.send(
                f"Your tag: `{tag_name}` has been denied on the Grim Dawn server."
            )
            await interaction.message.channel.send(
                f"Tag `{tag_name}` denied by {interaction.user}."
            )
            await interaction.message.delete()

        deny_button.callback = deny_callback

        buttons.add_item(item=approval_button)
        buttons.add_item(item=deny_button)
        return buttons

    def create_embed(self, interaction: discord.Interaction, tag, data):
        tag_embed = discord.Embed(
            title="New Tag Submission",
            type="rich",
            description="Key: " + tag,
            color=0x00FFFF,
        )
        tag_embed.set_author(
            name=interaction.user, icon_url=interaction.user.avatar.url
        )
        tag_embed.add_field(name="Content", value="Value: " + data, inline=False)
        tag_embed.add_field(
            name="Author ID", value=str(interaction.user.id), inline=False
        )
        return tag_embed
