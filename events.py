import discord
from discord.ext import commands
import random


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
        if message.content.replace(" ", "") == "🤔😉":
            await message.channel.send("<:winking:359819933711859713>")
            await message.delete()