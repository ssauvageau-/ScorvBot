import base64
import copy
import os
import json
from typing import Dict, List

import discord
from discord.ui import Button
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv


@app_commands.guild_only()
class TagSystemGroup(app_commands.Group, name="tag"):
    def __init__(self, bot: commands.Bot):
        load_dotenv()
        self.tag_json_path = os.getenv("TAG_JSON_PATH")
        try:
            self.tag_dict = self.load_tags()
        except json.decoder.JSONDecodeError:
            self.tag_dict = {}
        except FileNotFoundError:
            self.tag_dict = {}
            if not os.path.exists("json"):
                os.makedirs("json")
            os.close(os.open(self.tag_json_path, os.O_CREAT))
        self.approval_channel = os.getenv("TAG_APPROVAL_ID")
        self.bot = bot
        super().__init__()

    def load_tags(self) -> Dict[str, Dict]:
        with open(self.tag_json_path, "r", encoding="utf-8") as disk_lib:
            return json.loads(disk_lib.read())

    def dump_tags(self) -> None:
        with open(self.tag_json_path, "w", encoding="utf-8") as disk_lib:
            disk_lib.write(json.dumps(self.tag_dict, sort_keys=True))

    def encode_tag_data(self, data: str) -> str:
        return base64.b64encode(data.encode("utf-8")).decode("utf-8")

    def decode_tag_data(self, data: str) -> str:
        return base64.b64decode(data.encode("utf-8")).decode("utf-8")

    async def tag_autocomplete(
        self, interaction: discord.Interaction, current: str
    ) -> List[app_commands.Choice[str]]:
        choices = [*self.tag_dict]
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
        data = self.tag_dict[choice]["data"]
        decoded_data = self.decode_tag_data(data)
        await interaction.response.send_message(decoded_data)

    @app_commands.command(name="submit", description="Submit a new tag for review.")
    async def submit_tag(
        self, interaction: discord.Interaction, tag: str, content: str
    ):
        tag_clean = tag.strip()
        content_clean = content.strip()
        if tag_clean in self.tag_dict:
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
        if tag_clean in self.tag_dict:
            # Deep clone in place so as not to interfere with other async funcs that may be reading dict at time
            clone = copy.deepcopy(self.tag_dict)
            del clone[tag_clean]
            self.tag_dict = clone
            self.dump_tags()
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
        self, submission: discord.Interaction, tag: str, data: str
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
                f"Your tag: `{tag}` has been approved on the Grim Dawn server!"
            )
            await interaction.message.channel.send(
                f"Tag `{tag}` approved by {interaction.user}."
            )
            encoded_data = self.encode_tag_data(data)
            self.tag_dict[tag] = {
                "data": encoded_data,
                "author": interaction.user.name,
                "creation": interaction.created_at.strftime("%a %d %b %Y, %I:%M%p %Z"),
            }
            self.dump_tags()
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
                f"Your tag: `{tag}` has been denied on the Grim Dawn server."
            )
            await interaction.message.channel.send(
                f"Tag `{tag}` denied by {interaction.user}."
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
