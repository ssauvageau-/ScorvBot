import base64
import os
import json

import discord
from discord.ui import Button
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv


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
            await self.bot.get_channel(int(self.approval_channel)).send(
                embed=create_embed(interaction, tag_clean, content_clean),
                view=await create_approval_buttons(self, interaction, tag_clean, content_clean)
            )
            await interaction.response.send_message("Tag " + tag_clean + " has been submitted for review.")
            return


def load_tags(fn):
    with open(fn) as disk_lib:
        return json.loads(disk_lib.read())

def dump_tags(fn, tags):
    with open(fn, 'w') as disk_lib:
        disk_lib.write(json.dumps(tags, sort_keys=True))


async def create_approval_buttons(self, submission: discord.Interaction, tag, data):
    buttons = discord.ui.View(timeout=None)
    approval_button = Button(
        style=discord.ButtonStyle.green,
        label="Approve",
        custom_id='approve_button',
        disabled=False,
        emoji='👍',
        row=1
    )

    async def approval_callback(interaction: discord.Interaction):
        # We don't use this Interaction but Discord *will* send it into our override, so we need to catch it
        #await submission.user.send(f"Your tag: \"!{tag}\" has been approved on the Grim Dawn server!")
        await interaction.message.channel.send(f"Tag {tag} approved by {interaction.user}.")
        self.tagDict[tag] = data
        dump_tags(os.getenv("TAG_JSON_PATH"), self.tagDict)
        await interaction.message.delete()
    approval_button.callback = approval_callback

    deny_button = Button(
        style=discord.ButtonStyle.red,
        label="Deny",
        custom_id='deny_button',
        disabled=False,
        emoji='👎',
        row=1
    )

    async def deny_callback(interaction: discord.Interaction):
        # We don't use this Interaction but Discord *will* send it into our override, so we need to catch it
        await submission.user.send(f"Your tag: \"!{tag}\" has been denied on the Grim Dawn server.")
        await interaction.message.channel.send(f"Tag {tag} denied by {interaction.user}.")
        await interaction.message.delete()
    deny_button.callback = deny_callback

    buttons.add_item(item=approval_button)
    buttons.add_item(item=deny_button)
    return buttons


def create_embed(interaction: discord.Interaction, tag, data):
    tag_embed = discord.Embed(
        title="New Tag Submission",
        type="rich",
        description="Key: " + tag,
        color=0x00FFFF
    )
    tag_embed.set_author(
        name=interaction.user,
        icon_url=interaction.user.avatar.url
    )
    tag_embed.add_field(
        name="Content",
        value="Value: " + data,
        inline=False
    )
    tag_embed.add_field(
        name="Author ID",
        value=str(interaction.user.id),
        inline=False
    )
    return tag_embed
