import random

import discord
from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener(name="on_message")
    async def nerd_event(self, message: discord.Message):
        if message.author == self.bot.user:
            return

        if message.content == "nerd":
            await message.channel.send("nerd")
            await message.delete()

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
                    ]
                )
            )

    @commands.Cog.listener(name="on_message")
    async def thinkematic_event(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        pruned = message.content.replace(" ", "")
        match pruned:
            case "🤔😉":
                await message.channel.send("<:winking:359819933711859713>")
                await message.delete()
            case "🤔🇯🇵":
                await message.channel.send("<:weebthink:359798823725432842>")
                await message.delete()
            case "🤔🖕":
                await message.channel.send("<:upthink:359820561305829386>")
                await message.delete()
            case "🤔☯":
                await message.channel.send("<:thinkyang:359822049650147339>")
                await message.delete()
            case "🤔🌊":
                await message.channel.send("<:thinkwave:359800247876059139>")
                await message.delete()
            case "🤔✝️":
                await message.channel.send("<:thinkusVult:537783872595689487>")
                await message.delete()
            case "🤔👍":
                await message.channel.send("<:thinkup:359823000159387649>")
                await message.delete()
            case "🤔😐":
                await message.channel.send("<:thinkstare:359820274532614144>")
                await message.delete()
            case "🤔🔄":
                await message.channel.send("<a:fidgetthink:1153410621057011762>")
                await message.delete()
            case "🤔🔃":
                await message.channel.send("<a:fidgetthink_alt:1153411438271013065>")
                await message.delete()
            case "🤔😡":
                await message.channel.send("<:thinkrage:359798824404910080>")
                await message.delete()
            case "🤔🍆":
                await message.channel.send("<:thinkplant:359822667655938048>")
                await message.delete()
            case "🤔💻":
                await message.channel.send("<:thinkpad:359821250484502540>")
                await message.delete()
            case "🤔😕":
                await message.channel.send("<:thinkfusing:359822865584881690>")
                await message.delete()
            case "🤔🐟":
                await message.channel.send("<:thinkfish:359822611191955466>")
                await message.delete()
            case "🤔💦":
                await message.channel.send("<:thinkdrops:359821539392225291>")
                await message.delete()
            case "🤔🤔":
                await message.channel.send("<:thinkception:359822479147008000>")
                await message.delete()
            case "🤔⬜":
                await message.channel.send("<:squarethink:359821163817467904>")
                await message.delete()
            case "🤔🥔":
                await message.channel.send("<:spudthink:347098778647658515>")
                await message.delete()
            case "🤔🦀":
                await message.channel.send("<:ok_thinking:359798825763995648>")
                await message.delete()
            case "🤔🎩":
                await message.channel.send("<:mthinking:359821640340733952>")
                await message.delete()
            case "🤔👈":
                await message.channel.send("<:leftythink:359821079264624640>")
                await message.delete()
            case "🤔👏":
                await message.channel.send("<:clapking:359798826388815889>")
                await message.delete()
            case "🤔🍞":
                await message.channel.send("<:breading:359821383401865228>")
                await message.delete()
            case "🤔🍺":
                await message.channel.send("<:beerthink:359821722439909376>")
                await message.delete()
            case "🤔😫":
                await message.channel.send("<:thinkyawn:359821867634393089>")
                await message.delete()
            case "🤔🍿":
                await message.channel.send("<:thinkcorn:376774691144204288>")
                await message.delete()
            case "🤔🅱️":
                await message.channel.send("<:bhinking:537783061656371220>")
                await message.delete()
            case "🤔💩":
                await message.channel.send("<:poopthink:538566107687288862>")
                await message.delete()
            case "<:thonking:327364004211064832><:thonking:327364004211064832>":
                await message.channel.send("<a:thonkered:540696116069400607>")
                await message.delete()
