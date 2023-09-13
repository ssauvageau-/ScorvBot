# bot.py
# DO NOT REMOVE COMMENTED OR UNUSED IMPORTS
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

async def in_guild(ctx):
    return ctx.guild is not None


@bot.command(aliases=['commandList', 'commands'])
async def _help(ctx):
    await ctx.send(embed=embeds.help_embed)


@bot.command(aliases=['rabagur', 'praise'])
async def praise_rabagur(ctx):
    with open("images/rabagur.png", "rb") as fh:
        f = discord.File(fh, filename="images/rabagur.png")
    await ctx.channel.send(file=f)
    await ctx.message.delete()


@bot.command(aliases=['nicememe', 'nice-meme', 'nm'])
async def nice_meme(ctx):
    with open("images/scorvmeme.png", "rb") as fh:
        f = discord.File(fh, filename="images/scorvmeme.png")
    await ctx.channel.send(file=f)
    await ctx.message.delete()


@commands.has_permissions(manage_messages=True)
@bot.command(aliases=['post-rules'])
async def post_rules(ctx, arg):
    if ctx.author.id == OWNER_ID or ctx.author.id == SUB_OWNER:
        id = int(arg)
        channel = bot.get_channel(id)
        if channel:
            await channel.purge()
            await channel.send("https://cdn.discordapp.com/attachments/428832869398347776/1151199255990640721/Grim_Dawn_Discord_Logo.png")
            await channel.send("https://cdn.discordapp.com/attachments/647753999948185611/647754106492026902/2a8e119d-e266-40d3-a9c8-a92194b658472Fdivider2.png")
            await channel.send(embed=embeds.welcome_embed)
            await channel.send("https://cdn.discordapp.com/attachments/647753999948185611/647754112661848094/2a8e119d-e266-40d3-a9c8-a92194b658472Fatt.png")
            await channel.send(embed=embeds.global_embed)
            await channel.send("https://cdn.discordapp.com/attachments/647753999948185611/647754128541614090/2a8e119d-e266-40d3-a9c8-a92194b658472Fchannel_rules.png")
            await channel.send(embed=embeds.channel_news_embed)
            await channel.send(embed=embeds.channel_gd_embed)
            await channel.send(embed=embeds.channel_community_embed)
            await channel.send(embed=embeds.channel_offtopic_embed)
            await channel.send("https://cdn.discordapp.com/attachments/647753999948185611/647754159034204160/2a8e119d-e266-40d3-a9c8-a92194b658472Fchat_roles.png")
            await channel.send(embed=embeds.chat_roles_embed)
        else:
            await ctx.message.channel.send("Channel ID " + arg + " does not exist!")
    else:
        await ctx.message.channel.send("Nice try, kiddo!")

@commands.has_permissions(manage_messages=True)
@bot.command(aliases=['post-links'])
async def post_links(ctx, arg):
    if ctx.author.id == OWNER_ID or ctx.author.id == SUB_OWNER:
        id = int(arg)
        channel = bot.get_channel(id)
        if channel:
            await channel.purge()
            await channel.send("https://cdn.discordapp.com/attachments/647753999948185611/647754188469567488/2a8e119d-e266-40d3-a9c8-a92194b658472Fbuy_now.png")
            await channel.send(embed=embeds.buy_gd_embed)
            await channel.send(embed=embeds.buy_aom_embed)
            await channel.send(embed=embeds.buy_fg_embed)
            await channel.send(embed=embeds.buy_foa_embed)
            await channel.send("https://cdn.discordapp.com/attachments/647753999948185611/647754218198925312/2a8e119d-e266-40d3-a9c8-a92194b658472Flinkbase.png")
            await channel.send(embed=embeds.links_embed)
        else:
            await ctx.message.channel.send("Channel ID " + arg + " does not exist!")
    else:
        await ctx.message.channel.send("Nice try, kiddo!")


@bot.command(aliases=['quit', 'q'])
async def shutdown(ctx):
    if ctx.author.id == OWNER_ID or ctx.author.id == SUB_OWNER:
        await ctx.message.delete()
        await ctx.bot.close()
    else:
        await ctx.message.channel.send("Nice try, kiddo!")


bot.run(TOKEN)
