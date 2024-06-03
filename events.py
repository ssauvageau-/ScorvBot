import logging
import random
import re

import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timezone

from utils import Sunder, log_utils

utc = timezone.utc


class Events(commands.Cog, name="Events"):
    def __init__(self, bot: commands.Bot) -> None:
        self.logger = logging.getLogger("bot")
        self.log_channel_name = "scorv-log"
        self.log_channel_name_alt = "scorv-log2"
        self.bot = bot
        self.timeline = {}

    @commands.Cog.listener(name="on_error")
    async def log_error(self, event: str, *args, **kwargs):
        self.logger.error(event)

    @commands.Cog.listener(name="on_app_command_completion")
    async def log_app_command_completion(
        self, interaction: discord.Interaction, command: app_commands.Command
    ):
        self.logger.info(
            f"User {log_utils.format_user(interaction.user)} used command {log_utils.format_app_command_name(command)} in {log_utils.format_channel_name(interaction.channel)}"
        )

    # @commands.Cog.listener(name="on_message")
    # async def fish_event(self, message: discord.Message):
    #     if message.author == self.bot.user:
    #         return
    #
    #     if message.author.id in (
    #         225337962521427968,
    #         274230000935370763,
    #     ):  # Zantai, mad_lee
    #         if random.randint(1, 200) == 69:
    #             await message.channel.send("<:lawyerfish:1156268220546826321>")
    #     elif message.author.id in (
    #         434082239706431508,  # Maska
    #         136586501436735488,  # Ceno
    #         297721856130154497,  # Mergo
    #         # 587334964257751053,  # Avyctes
    #         406040451850698752,  # Snazzymoistboi
    #     ):
    #         if random.randint(1, 500) == 69:
    #             await message.channel.send("<:lawyerfish:1156268220546826321>")

    @commands.Cog.listener(name="on_message")
    async def peach_event(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        if message.author.id in (
            142134189800685568,  # Eard
            406040451850698752,  # Snazzymoistboi
        ):
            if "butt" in message.content.lower():
                await message.add_reaction(
                    random.choice(
                        [
                            "🍑",
                            "<:ass:649476166750568478>",
                            "<:assL:649819612417884182>",
                            "<:buttdevotions:792203000008933426>",
                        ]
                    )
                )
                self.logger.info(f"butt event triggered on message {message.jump_url}")

    @commands.Cog.listener(name="on_message")
    async def tomo_event(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        if message.author.id == 255472765434331147:
            if random.randint(1, 100) == 69:
                stickers = message.guild.stickers
                tomo = [sticker for sticker in stickers if sticker.name == "tomodak"]
                await message.channel.send(stickers=tomo)
                self.logger.info(f"Tomo event triggered on message {message.jump_url}")

    @commands.Cog.listener(name="on_message")
    async def nerd_event(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        if message.content.lower() == "nerd":
            await message.channel.send(message.content)
            await message.delete()
            self.logger.info(f"nerd event triggered on message {message.jump_url}")

    @commands.Cog.listener(name="on_message")
    async def crab_event(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        if "crab" in message.content.lower():
            await message.add_reaction(
                random.choice(
                    [
                        "🦀",
                        "<:crabDevotion:796803035904606250>",
                        "<a:crabPls:649476167266467842>",
                        "<:crabdab:1212416997921398784>",
                        "<:crabbostabbo:1212417029613813810>",
                    ]
                )
            )
            self.logger.info(f"crab event triggered on message {message.jump_url}")

    @commands.Cog.listener(name="on_message")
    async def xpac_event(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        if "xpacwhen" in message.content.replace(" ", "").lower():
            await message.reply(
                content="https://cdn.discordapp.com/attachments/1151691325549322262/1153779612053159946/image.png"
            )
            self.logger.info(f"xpac event triggered on message {message.jump_url}")

    @commands.Cog.listener(name="on_message")
    async def thinkematic_event(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        thinkematics_tm = {
            "🤔😉": "<:winking:359819933711859713>",
            "🤔🇯🇵": "<:weebthink:359798823725432842>",
            "🤔🖕": "<:upthink:359820561305829386>",
            "🤔☯": "<:thinkyang:359822049650147339>",
            "🤔🌊": "<:thinkwave:359800247876059139>",
            "🤔✝️": "<:thinkusVult:537783872595689487>",
            "🤔👍": "<:thinkup:359823000159387649>",
            "🤔😐": "<:thinkstare:359820274532614144>",
            "🤔🔄": "<a:fidgetthink:1153410621057011762>",
            "🤔🔃": "<a:fidgetthink_alt:1153411438271013065>",
            "🤔😡": "<:thinkrage:359798824404910080>",
            "🤔🍆": "<:thinkplant:359822667655938048>",
            "🤔💻": "<:thinkpad:359821250484502540>",
            "🤔😕": "<:thinkfusing:359822865584881690>",
            "🤔🐟": "<:thinkfish:359822611191955466>",
            "🤔💦": "<:thinkdrops:359821539392225291>",
            "🤔🤔": "<:thinkception:359822479147008000>",
            "🤔⬜": "<:squarethink:359821163817467904>",
            "🤔🥔": "<:spudthink:1160997520474902569>",
            "🤔🦀": "<:crabthink:1175152963199701062>",
            "🤔🎩": "<:mthinking:359821640340733952>",
            "🤔👈": "<:leftythink:359821079264624640>",
            "🤔👏": "<:clapking:359798826388815889>",
            "🤔🍞": "<:breading:359821383401865228>",
            "🤔🍺": "<:beerthink:359821722439909376>",
            "🤔😫": "<:thinkyawn:359821867634393089>",
            "🤔🍿": "<:thinkcorn:376774691144204288>",
            "🤔🅱️": "<:bhinking:537783061656371220>",
            "🤔💩": "<:poopthink:538566107687288862>",
            "🤔👀": "<:thinkeyes:359798823486226443>",
            "🤔👌": "<:ok_thinking:359798825763995648>",
            "🤔⬆️⬆️⬇️⬇️⬅️➡️⬅️➡️🇧🇦": f"{message.author.mention} is a nerd! 🤓",
            "<:thonking:327364004211064832><:thonking:327364004211064832>": "<a:thonkered:540696116069400607>",
            "🤔🐦": "<:mayayy:1153451055657517077>",
            "🤔🔥": "<:finethink:1153504940178817034>",
            "<:kappaScorv:562136888731762688><:kappaScorv:562136888731762688>": "<:scorvChaos:655350057205235712>",
            "<:kappaScorv:562136888731762688>🔫": "<:scorvgun:792202763379015681>",
        }

        pruned = message.content.replace(" ", "")
        think = thinkematics_tm.get(pruned)
        if think is not None:
            think_message = await message.channel.send(think)
            await message.delete()
            self.logger.info(
                f"Thinkematics {think} triggered by {message.author.display_name} {think_message.jump_url}"
            )

    @commands.Cog.listener(name="on_message")
    async def sunder_event(self, message: discord.Message):
        if message.author.bot:
            return

        sundered = discord.utils.find(
            lambda role: role.name == "Sundered", message.author.roles
        )
        if sundered is not None:
            return

        threshold = 0.98 if "sunder" in message.content else 1
        # too lazy to remove this if statement; random.random() cannot roll 1.0 so this disables any message being able to sunder

        if random.random() >= threshold:
            sundered_role = discord.utils.find(
                lambda role: role.name == "Sundered", message.guild.roles
            )

            async with Sunder(message.author) as sunder:
                sunder_message = await message.channel.send(
                    file=sunder[0], embed=sunder[1]
                )
                await message.author.add_roles(sundered_role, reason="Sundered")
                self.logger.info(
                    f"Sundered {message.author.display_name} {sunder_message.jump_url}"
                )

    @commands.Cog.listener(name="on_message")
    async def masked_url_event(self, message: discord.Message):
        if message.author.bot:
            return

        log_channel = discord.utils.find(
            lambda channel: channel.name == self.log_channel_name,
            message.guild.channels,
        )
        if log_channel is None:
            raise Exception("Log channel not found")

        masked_url_pattern = r"\[(?P<mask>.+)\]\((?P<url>.*)\)"
        for masked_url in re.finditer(masked_url_pattern, message.content):
            mask = masked_url.group("mask")
            url = masked_url.group("url")

            steam = "steamcommunity.com/" in mask.lower()

            log_embed = discord.Embed(
                color=discord.Color.red() if steam else discord.Color.yellow(),
                title="Steam URL Mask Detected & Deleted"
                if steam
                else "Masked URL in message",
                description=message.author.mention,
                timestamp=message.created_at,
            )
            log_embed.set_author(
                name=message.author.display_name,
                icon_url=message.author.display_avatar.url,
            )
            if not steam:
                log_embed.add_field(name="Message", value=message.jump_url, inline=True)
            log_embed.add_field(name="Mask", value=f"`{mask}`", inline=True)
            log_embed.add_field(name="URL", value=f"`{url}`", inline=True)

            await log_channel.send(embed=log_embed)
            if not steam:
                self.logger.info(
                    f"Masked URL [{mask}]({url}) posted in {log_utils.format_channel_name(message.channel)} {message.jump_url}"
                )
            else:
                self.logger.info(
                    f"Steam URL Mask [{mask}]({url}) posted in {log_utils.format_channel_name(message.channel)}. Message Deleted."
                )
                await message.delete()

    @commands.Cog.listener(name="on_message")
    async def discord_link_event(self, message: discord.Message):
        if message.author.bot:
            return

        roles = []
        for role in message.author.roles:
            if role.name in ["Admin", "Moderator"]:
                return

        log_channel = discord.utils.find(
            lambda channel: channel.name == self.log_channel_name,
            message.guild.channels,
        )
        if log_channel is None:
            raise Exception("Log channel not found")

        whitelist = [
            "8Dr8mge",  # Grim Dawn
            "WbBWWuAYjh",  # Farthest Frontier
            "n94PcmV",  # GD League
            "8uEhMAkxHc",  # Dammitt's Tools
            "GNqqDUz",  # Grimarillion & DoM
        ]

        if (
            "discord.gg/" in message.content.lower()
            or "discord.com/invite/" in message.content.lower()
            or "discordapp.com/invite/" in message.content.lower()
        ):
            for approved in whitelist:
                if approved in message.content.lower():
                    return

            log_embed = discord.Embed(
                color=discord.Color.red(),
                title="Discord Link Posted",
                description=message.author.mention,
                timestamp=message.created_at,
            )
            log_embed.set_author(
                name=message.author.display_name,
                icon_url=message.author.display_avatar.url,
            )
            log_embed.add_field(
                name="Channel", value=message.channel.jump_url, inline=True
            )
            log_embed.add_field(name="Message", value=message.content, inline=True)

            await log_channel.send(embed=log_embed)
            self.logger.info(
                f"Discord link posted in {log_utils.format_channel_name(message.channel)} by {log_utils.format_user(message.author)}"
            )
            await message.reply(
                content=f"{message.author.display_name} - please do not share Discord links in this server! Thank you! :)"
            )
            await message.delete()

    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ):
        log_channel = None
        if before.channel is not None:
            log_channel = discord.utils.find(
                lambda channel: channel.name == self.log_channel_name_alt,
                before.channel.guild.channels,
            )
        elif after.channel is not None:
            log_channel = discord.utils.find(
                lambda channel: channel.name == self.log_channel_name_alt,
                after.channel.guild.channels,
            )
        if log_channel is None:
            raise Exception("Log channel not found")

        if (
            before.channel is None and after.channel is not None
        ):  # user was not in voice but is now
            self.timeline[member] = {
                "last_channel": after.channel,
                "connected": datetime.now(tz=utc),
                "disconnected": None,
                "hops": [],
            }
            await log_channel.send(
                content=f"<t:{int(datetime.now(tz=utc).timestamp())}:R>\t{member.mention} joined {after.channel.name}."
            )
            self.logger.info(
                f"{log_utils.format_user(member)} joined {after.channel.name}"
            )
            # a member is a user; log_utils wants a discord.User here, so warning given by IDE. Make a format_member
            # func that is identical in function to format_user?
        elif (
            before.channel is not None and after.channel is not None
        ):  # user hopped from one channel to another
            self.timeline[member].update(
                {
                    "last_channel": after.channel,
                }
            )
            now = datetime.now(tz=utc)
            self.timeline[member]["hops"].append(
                {
                    "channel": before.channel,
                    "disconnected": now,
                }
            )
            self.logger.info(
                f"{log_utils.format_user(member)} joined {after.channel.name} from {before.channel.name}."
            )
        elif (
            before.channel is not None and after.channel is None
        ):  # user has disconnected from voice
            self.timeline[member].update({"disconnected": datetime.now(tz=utc)})

            hist = self.timeline.pop(
                member, None
            )  # pop to remove entry from dict, but use it below
            diff = hist["disconnected"] - hist["connected"]
            await log_channel.send(
                content=f"<t:{int(datetime.now(tz=utc).timestamp())}:R>\t{member.mention} disconnected from {before.channel.name} after {diff} in total."
            )
            self.logger.info(
                f"{log_utils.format_user(member)} disconnected from {before.channel.name} after {diff} in total."
            )
