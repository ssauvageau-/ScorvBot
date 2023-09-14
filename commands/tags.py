import os

import discord
import discord.ui.button
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import json

tagDict = {}


@app_commands.guild_only()
class TagSystemGroup(app_commands.Group, name="tag"):
    def __init__(self, bot: commands.Bot):
        load_dotenv()
        self.tagDict = load_tags(os.getenv("TAG_JSON_PATH"))
        self.approval_channel = os.getenv("TAG_APPROVAL_ID")
        self.bot = bot
        super().__init__()

    @app_commands.command(
        name="submit", description="Submit a new tag for review."
    )
    async def submit_tag(
            self, interaction: discord.Interaction, tag: str, content: str
    ):
        tag_clean = tag.strip()
        content_clean = content.strip()
        if tag_clean in self.tagDict:
            await interaction.response.send_message("Tag " + tag_clean + " already exists!")
            return
        else:  # redundant but indented for clarity
            await self.bot.get_channel(int(self.approval_channel)).send(embed=create_embed(interaction, tag_clean, content_clean))
            await interaction.response.send_message("Tag " + tag_clean + " has been submitted for review.")
            return


def load_tags(fn):
    with open(fn) as disk_lib:
        return json.load(disk_lib)


def create_embed(interaction: discord.Interaction, tag, data):
    tag_embed = discord.Embed(
        title="New Tag Submission",
        type="rich",
        description=tag,
        color=0x00FFFF
    )
    tag_embed.set_author(
        name=interaction.user,
        icon_url=interaction.user.avatar.url
    )
    tag_embed.add_field(
        name="Content",
        value=data,
        inline=False
    )
    tag_embed.add_field(
        name="Author ID",
        value=str(interaction.user.id),
        inline=False
    )
    return tag_embed
