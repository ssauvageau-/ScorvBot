""" DEPRECATED
# bot.py
import ast
import os
import io
from os.path import exists
import sys
import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound, CheckFailure
from discord.utils import get
import json
# noinspection PyUnresolvedReferences
from dotenv import load_dotenv
import embeds

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
OWNER_ID = int(os.getenv('DISCORD_OWNER'))
SUB_OWNER = int(os.getenv('DISCORD_SUBOWNER'))
intents = discord.Intents.all()
intents.members = True
PREFIX = '!'
COMMAND_WHITELIST = {"Admin", "Moderator"}

bot = commands.Bot(command_prefix=PREFIX, intents=intents)


@bot.command(aliases=['commandList', 'commands'])
async def _help(ctx):
    await ctx.send(embed=embeds.help_embed)


bot.run(TOKEN)
"""
