import os
from typing import Optional

from PIL import Image, ImageSequence
import discord
from discord import app_commands
from discord.ext import commands

from utils import Sunder


@app_commands.guild_only()
class MiscCommandCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.mobile_path = "images/MobileDiscord.png"
        self.embed_path = "images/EmbedDiscord.png"
        self.log_channel = "scorv-log"
        super().__init__()

    @app_commands.command(name="f", description="Pay respects. 'to' is optional.")
    async def pay_respects(
        self, interaction: discord.Interaction, to: Optional[str] = None
    ):
        if to:
            await interaction.response.send_message(
                f"Press 🇫 to pay respects to {to}{'' if to.endswith('.') else '.'}"
            )
        else:
            await interaction.response.send_message("Press 🇫 to pay respects.")
        response = await interaction.original_response()
        await response.add_reaction("🇫")

    @app_commands.command(
        name="scorv-post", description="Send a text message as Scorv! Limited access!"
    )
    @app_commands.checks.has_any_role(
        "Admin", "Moderator", "Janitor", "Crate Entertainment"
    )
    async def scorv_post(self, interaction: discord.Interaction, message: str):
        # is limited role access to this necessary given the moderation log channel setup?
        # TODO unrelated here, but refactor tags/rules/links channels (#tag-approval, #rules, #links) to use this way
        # TODO of finding channels by name instead of hardcoded channel IDs/passing ID as argument on call?
        log = discord.utils.find(
            lambda c: c.name == self.log_channel, interaction.guild.channels
        )
        if log:
            await interaction.response.send_message(
                "Sending your message below:", ephemeral=True
            )
            post_message = await interaction.channel.send(message)
            await log.send(
                f"{interaction.user} sent a post as Scorv: {message} -> {post_message.jump_url}"
            )
            return
        # else - log channel not found
        await interaction.response.send_message(
            "Could not find moderation log channel, cannot send anonymized message in public!",
            ephemeral=True,
        )

    @app_commands.command(
        name="quote", description="Quote a previous message through the bot."
    )
    async def quote(self, interaction: discord.Interaction, link: str):
        # https: // discord.com / channels / 119758608765288449 / 428832869398347776 / 1161002383996883058
        # 119758608765288449 / 428832869398347776 / 1161002383996883058
        # GUILD / CHANNEL / MESSAGE
        msg = link.split("/")
        guild = interaction.guild
        channel_id = int(msg[5])
        message_id = int(msg[6])
        channel = guild.get_channel(channel_id)
        message = await channel.fetch_message(message_id)
        tmp_embed = discord.Embed(
            color=message.author.color, timestamp=message.created_at
        )
        tmp_embed.add_field(name="", value=message.content, inline=False)
        tmp_embed.set_footer(text=channel.name)
        tmp_embed.set_author(
            name=message.author.name, icon_url=message.author.avatar, url=link
        )
        await interaction.response.send_message(embed=tmp_embed)

    @app_commands.command(name="mobile")
    async def mobile_image(self, interaction: discord.Interaction, user: discord.User):
        avatar = user.display_avatar
        fn = str(user.id) + "_temp"
        fn_o = "mobile_output.gif"
        frame_list = []
        await avatar.save(fn)
        with Image.open(fn) as im:
            idx = 1
            duration = 0

            for frame in ImageSequence.Iterator(im):
                frame_list.append(self.build_frame(frame, self.mobile_path))
                idx += 1
                try:
                    duration += im.info["duration"]
                except KeyError:
                    continue

            frame_duration = int(idx / duration) if duration > 0 else 1000

        frame_list[0].save(
            fn_o,
            save_all=True,
            append_images=frame_list[1:],
            optimize=False,
            duration=frame_duration,
            loop=0,
        )

        await interaction.response.send_message(file=discord.File(fp=fn_o))

        if os.path.exists(fn):
            os.remove(fn)
        else:
            print(f"Error occurred when deleting file:\t{fn}")
        if os.path.exists(fn_o):
            os.remove(fn_o)
        else:
            print(f"Error occurred when deleting file:\t{fn_o}")

    @app_commands.command(name="embed")
    async def embed_image(self, interaction: discord.Interaction, user: discord.User):
        avatar = user.display_avatar
        fn = str(user.id) + "_temp"
        fn_o = "embed_output.gif"
        frame_list = []
        await avatar.save(fn)
        with Image.open(fn) as im:
            idx = 1
            duration = 0

            for frame in ImageSequence.Iterator(im):
                frame_list.append(self.build_frame(frame, self.embed_path))
                idx += 1
                try:
                    duration += im.info["duration"]
                except KeyError:
                    continue

            frame_duration = int(idx / duration) if duration > 0 else 1000

        frame_list[0].save(
            fn_o,
            save_all=True,
            append_images=frame_list[1:],
            optimize=False,
            duration=frame_duration,
            loop=0,
        )

        await interaction.response.send_message(file=discord.File(fp=fn_o))

        if os.path.exists(fn):
            os.remove(fn)
        else:
            print(f"Error occurred when deleting file:\t{fn}")
        if os.path.exists(fn_o):
            os.remove(fn_o)
        else:
            print(f"Error occurred when deleting file:\t{fn_o}")

    def build_frame(self, icon, path):
        mobile_discord = Image.open(path)
        iresize = icon.resize((43, 43), Image.LANCZOS)
        x1, y1 = 221, 148
        x2, y2 = 264, 191
        mask = iresize.convert("RGBA")
        mobile_discord.paste(iresize, (x1, y1, x2, y2), mask)
        return mobile_discord

    @app_commands.command(
        name="sunder",
        description="Sunder a member which temporarly gives them a 'Sundered' role and posts a message in the channel.",
    )
    @app_commands.describe(member="The member to sunder")
    @app_commands.checks.has_any_role("Admin", "Moderator", "Janitor")
    async def sunder(
        self, interaction: discord.Interaction, member: discord.Member
    ) -> None:
        await interaction.response.defer(ephemeral=True, thinking=True)

        sundered_role = discord.utils.find(
            lambda role: role.name == "Sundered", interaction.guild.roles
        )

        async with Sunder(member) as sunder:
            await interaction.channel.send(file=sunder[0], embed=sunder[1])
            await member.add_roles(sundered_role, reason="Sundered")
            await interaction.followup.send(
                f"Sundered {member.display_name}", ephemeral=True
            )
