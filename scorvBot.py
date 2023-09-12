# bot.py
# DO NOT REMOVE COMMENTED OR UNUSED IMPORTS
import ast
import os
from os.path import exists
import sys
import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound, CheckFailure
from discord.utils import get
import json
# noinspection PyUnresolvedReferences
from dotenv import load_dotenv
from contextlib import suppress

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
OWNER_ID = int(os.getenv('DISCORD_OWNER'))
SUB_OWNER = int(os.getenv('DISCORD_SUBOWNER'))
intents = discord.Intents.all()
intents.members = True
PREFIX = '!'

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

helpEmbed = discord.Embed(title="Command List", color=0xFF5733)
helpEmbed.add_field(
    name="commandList, commands", value="* Displays this help dialogue.", inline=False
)
helpEmbed.add_field(
    name="clear", value="Arguments: N (default=1)\n* Clears the previous N messages.", inline=False
)
helpEmbed.add_field(
    name="clear-commands, clear-c", value="Arguments: N (default=1)\n* Clears the previous N messages which begin "
                                          "with the command prefix (" + PREFIX + ").", inline=False
)
helpEmbed.add_field(
    name="create-channel, cc", value="Arguments: Name (required)\n* Creates a text channel called Name.", inline=False
)
helpEmbed.add_field(
    name="create-hidden-channel, chc", value="Arguments: Name (required), IDs (optional, supports multiple)\n"
                                             "* Creates a hidden text channel called Name that only those with the "
                                             "given IDs can view, along with the bot and the server owner.",
    inline=False
)
helpEmbed.add_field(
    name="create-hidden-channel-no-bot, chcnb", value="Arguments: Name (required), IDs (optional, supports multiple)\n"
                                                      "* Creates a hidden text channel called Name that only those with"
                                                      " the given IDs can view, along with the server owner.",
    inline=False
)
helpEmbed.add_field(
    name="create-role, new-role, cr", value="Arguments: Name (required)\n"
                                            "* Creates the Name role if it does not exist, or informs the user if it "
                                            "does.",
    inline=False
)
helpEmbed.add_field(
    name="delete-role, dr", value="Arguments: Name (required)\n"
                                  "* Deletes the role named Name, or informs the user that no such role exists.",
    inline=False
)
helpEmbed.add_field(
    name="help", value="* Generates the default discord.py help message with no documentation.",
    inline=False
)
helpEmbed.add_field(
    name="quit, q", value="* Shuts down the bot."
                          "\n\nOnly the bot author can use this command.",
    inline=False
)

welcome_embed = discord.Embed(color=0x1E1F22)
welcome_embed.add_field(
    name="Welcome to the Community Grim Dawn Discord Server",
    value="Grim Dawn is an ARPG set inside a apocalyptic fantasy world where humanity is on the brink of extinction, "
          "iron is valued above gold and trust is hard earned. Grim Dawn features complex character development, "
          "hundreds of unique items, crafting, and quests with choice & consequence.",
    inline=False
)
global_embed = discord.Embed(color=0x1E1F22)
global_embed.add_field(
    name="Global Rules",
    value="**1**. Follow the channel rules."
          "\n**2**. Be respectful to everyone."
          "\n**3**. Restrict yourself to english."
          "\n**4**. Posting pornographic, disturbing, illegal images/links is strictly prohibited."
          "\n**5**. There is no need to be upset about anything."
          "\n**6**. Moderators and Admins private message you for a reason, listen."
          "\n**7**. Do not advertise or encourage anything that is against the TOS/EULA of Grim Dawn."
          "\n**8**. Do not advertise any kind of Discord/community/campaign or other links without permission."
          "\n**9**. Check the links down below before asking for support.",
    inline=False
)
channel_news_embed = discord.Embed(color=0x1E1F22)
channel_news_embed.add_field(
    name="Global",
    value="<#137741704944943105>"
          "\nNews about recent important events related to Grim Dawn."
          "\n<#480494439564050443>"
          "\nThis channel will be updated with the official Crate Entertainment [Twitter](https://twitter.com/grimdawn)"
          " and [Twitch](https://www.twitch.tv/crateentertainment) account activity."
          "\n<#1150483398754836530>"
          "\nThis channel will be updated with updates to this server.",
    inline=False
)
channel_offtopic_embed = discord.Embed(color=0x1E1F22)
channel_offtopic_embed.add_field(
    name="↓ Offtopic ↓",
    value="<#119758608765288449>"
          "\nFor discussion of other games unrelated to Grim Dawn."
          "\n<#144781923590471680>"
          "\nEverything is allowed within range of the rules but use common sense."
          "\n<#602362713863094322>"
          "\nPost memes. Be ***respectful***, no clearly over the line offensive content please."
          "\n<#653698423945560075>"
          "\nFor sharing and discussing music, commonly through YouTube.",
    inline=False
)
channel_gd_embed = discord.Embed(color=0x1E1F22)
channel_gd_embed.add_field(
    name="↓ Grim Dawn ↓",
    value="<#340206431070322692>"
          "\nIs only meant to be about Grim Dawn."
          "\n<#474470028503285762>"
          "\nClosed community, open topic channel for <@&474151602454921218> members."
          "\n<#282754266123206657>"
          "\nThis channel is for Grim Dawn build discussions and helping each other with game related questions based "
          "on making your characters."
          "\n<#309941110128771073>"
          "\nAll about Grim Dawn mods and everything related."
          "\n(Other channels are not restricted to talk about mods for Grim Dawn.)",
    inline=False
)
channel_community_embed = discord.Embed(color=0x1E1F22)
channel_community_embed.add_field(
    name="↓ Community ↓",
    value="<#217995616163332096>"
          "\nThis channel is for the sole purpose of creating text posts with informations regarding the people you are searching to play with."
          "\n<#119761513148841984>"
          "\nThis channel is for the sole purpose of organizing item trades on softcore characters."
          "\nPlease use <LINK> if you are posting links."
          "\n<#1058431796460654683>"
          "\nThis channel is for the sole purpose of organizing item trades on hardcore characters."
          "\nPlease use <LINK> if you are posting links.",
    inline=False
)
chat_roles_embed = discord.Embed(color=0x1E1F22)
chat_roles_embed.add_field(
    name="",
    value="<@&241956541446619136>"
          "\nThe manager of this Discord server."
          "\nThis server's Discord moderation is not affiliated with Crate Entertainment."
          "\n<@&137735685674106880>"
          "\nHelps you with questions and keeps the Discord chat clean."
          "\n<@&351387211356438528>"
          "\nOur cleaning crew that enforces mostly channel rules."
          "\n<@&237159960566300672>"
          "\nOfficial Grim Dawn Forum moderator."
          "\n<@&340265796980703234>"
          "\nLong term community members with access to alpha versions of Grim Dawn to provide feedback and game testing results."
          "\nMost of them are giga-nerds."
          "\n<@&474151602454921218>"
          "\nPeople that have verified their forum account. Ask a moderator for instructions on how to do so if interested.",
    inline=False
)
buy_gd_embed = discord.Embed(color=0x322D28)
buy_gd_embed.add_field(
    name="",
    value="**Official Grim Dawn Website**"
          "\nhttps://www.grimdawn.com/"
          "\n**Steam**"
          "\nhttps://store.steampowered.com/app/219990/Grim_Dawn/"
          "\n**Humble Bundle**"
          "\nhttps://www.humblebundle.com/store/grim-dawn",
    inline=True
)
buy_gd_embed.set_image(url="https://media.discordapp.net/attachments/426464234994532364/557061415827931148/GD2.png")
buy_gd_embed.set_thumbnail(url="https://media.discordapp.net/attachments/426464234994532364/557061415827931148/GD2.png")
buy_aom_embed = discord.Embed(color=0x1D8863)
buy_aom_embed.add_field(
    name="",
    value="**Steam**"
          "\nhttps://store.steampowered.com/app/642280/Grim_Dawn__Ashes_of_Malmouth_Expansion/"
          "\n**Humble Bundle**"
          "\nhttps://www.humblebundle.com/store/grim-dawn-ashes-of-malmouth-expansion",
    inline=True
)
buy_aom_embed.set_image(url="https://media.discordapp.net/attachments/426464234994532364/557059808361054210/gdheaderboxtop_2.png")
buy_aom_embed.set_thumbnail(url="https://media.discordapp.net/attachments/426464234994532364/557059628802768897/aom_icon.png")
buy_fg_embed = discord.Embed(color=0xFFA647)
buy_fg_embed.add_field(
    name="",
    value="**Steam**"
          "\nhttps://store.steampowered.com/app/897670/Grim_Dawn__Forgotten_Gods_Expansion/"
          "\n**Humble Bundle**"
          "\nhttps://www.humblebundle.com/store/grim-dawn-forgotten-gods-expansion",
    inline=True
)
buy_fg_embed.set_image(url="https://media.discordapp.net/attachments/426464234994532364/557059372161957898/grimdawndiscordfg.png")
buy_fg_embed.set_thumbnail(url="https://media.discordapp.net/attachments/426464234994532364/557059472254566410/Grim_Dawn_0000.png")
buy_foa_embed = discord.Embed(color=0x60FFFC)
buy_foa_embed.add_field(
    name="",
    value="**Steam**"
          "\nComing Posthaste!"
          "\n**Humble Bundle**"
          "\nComing Posthaste!",
    inline=True
)
buy_foa_embed.set_image(url="https://cdn.discordapp.com/attachments/428832869398347776/1151193829869891739/gdx3_GD_icon_1.png")
buy_foa_embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/428832869398347776/1151193901013667880/cropped-gdx3_headerboxtop.png")
links_embed = discord.Embed(color=0x1E1F22)
links_embed.add_field(
    name="",
    value="**Official Links**"
          "\nGrim Dawn Forum"
          "\nhttps://forums.crateentertainment.com/c/grimdawn/"
          "\nGrim Dawn Builds"
          "\nhttps://forums.crateentertainment.com/c/grimdawn/classes-skills-and-builds/21"
          "\nGrim Dawn SubReddit"
          "\nhttps://www.reddit.com/r/Grimdawn/"
          "\nGrim Dawn Wikipedia"
          "\nhttps://grimdawn.fandom.com/wiki/Grim_Dawn_Wiki"
          "\n"
          "\n**Useful Links**"
          "\nGrim Dawn Online Map"
          "\nhttps://www.grimtools.com/map/"
          "\nGrim Dawn Build Compendium"
          "\nhttps://forums.crateentertainment.com/t/build-compendiums/82060"
          "\nGrim Dawn F.A.Q"
          "\nhttps://tinyurl.com/n676c8y"
          "\nCharacter Builder/Planner"
          "\nhttp://www.grimtools.com/calc/"
          "\nItem Database"
          "\nhttps://www.grimtools.com/db/items/"
          "\nMonster Database"
          "\nhttps://www.grimtools.com/monsterdb/"
          "\nResistance Reduction Cheat Sheet"
          "\nhttps://tinyurl.com/yya5hmo2"
)

async def in_guild(ctx):
    return ctx.guild is not None


@bot.event
async def on_ready():
    print("ScorvBot is now online.")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, (CommandNotFound, CheckFailure)): return
    if error == KeyboardInterrupt:
        await bot.close()
        return
    raise error


@bot.command(aliases=['commandList', 'commands'])
async def _help(ctx):
    await ctx.send(embed=helpEmbed)


@bot.command(aliases=['create-channel', 'cc'])
async def create_channel(ctx, arg):
    if ctx.author.id == OWNER_ID or ctx.author.id == SUB_OWNER:
        guild = ctx.guild
        existing_channel = discord.utils.get(guild.channels, name=arg)
        if not existing_channel:
            await guild.create_text_channel(arg)
        await ctx.message.delete()


@bot.command(aliases=['create-hidden-channel', 'chc', 'create-hidden'])
async def create_hidden_channel(ctx, arg, *args):
    if ctx.author.id == OWNER_ID or ctx.author.id == SUB_OWNER:
        guild = ctx.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True)
        }
        for id in [*args]:
            overwrites.update({guild.get_member(int(id)): discord.PermissionOverwrite(read_messages=True)})
        existing_channel = discord.utils.get(guild.channels, name=arg)
        if not existing_channel:
            await guild.create_text_channel(arg, overwrites=overwrites)
        await ctx.message.delete()


@bot.command(aliases=['create-hidden-channel-no-bot', 'chcnb'])
async def create_hidden_channel_no_bot(ctx, arg, *args):
    if ctx.author.id == OWNER_ID or ctx.author.id == SUB_OWNER:
        guild = ctx.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=False)
        }
        for id in [*args]:
            overwrites.update({guild.get_member(int(id)): discord.PermissionOverwrite(read_messages=True)})
        existing_channel = discord.utils.get(guild.channels, name=arg)
        if not existing_channel:
            await guild.create_text_channel(arg, overwrites=overwrites)
        await ctx.message.delete()


@bot.command(aliases=['create-role', 'new-role', 'cr'])
async def create_role(ctx, arg):
    if ctx.author.id == OWNER_ID or ctx.author.id == SUB_OWNER:
        guild = ctx.guild
        existing_role = discord.utils.get(guild.roles, name=arg)
        if not existing_role:
            await guild.create_role(name=arg)
            await ctx.message.delete()
        else:
            await ctx.message.channel.send("Role **" + arg + "** already exists!")


@bot.command(aliases=['delete-role', 'dr'])
async def delete_role(ctx, arg):
    if ctx.author.id == OWNER_ID or ctx.author.id == SUB_OWNER:
        guild = ctx.guild
        role = discord.utils.get(guild.roles, name=arg)
        if role:
            await role.delete()
            await ctx.message.delete()
        else:
            await ctx.message.channel.send("Role **" + arg + "** does not exist.")


@commands.has_permissions(manage_messages=True)
@bot.command(name='clear')
async def clear(ctx, number: int = 1):
    await ctx.message.delete()
    if ctx.author.id == OWNER_ID or ctx.author.id == SUB_OWNER:
        with suppress(AttributeError):
            channel: discord.TextChannel = ctx.channel
            if number > 100: number = 100
            async for m in channel.history(limit=number):
                await m.delete()


@commands.has_permissions(manage_messages=True)
@bot.command(aliases=['clear-commands', 'clear-c'])
async def clear_commands(ctx, number: int = 1):
    await ctx.message.delete()
    if ctx.author.id == OWNER_ID or ctx.author.id == SUB_OWNER:
        with suppress(AttributeError):
            channel: discord.TextChannel = ctx.channel
            if number > 100: number = 100
            async for m in channel.history(limit=number):
                if m.content[0] == "!":
                    await m.delete()


@commands.has_permissions(manage_messages=True)
@bot.command(aliases=['post-rules'])
async def post_rules(ctx, arg):
    if ctx.author.id == OWNER_ID or ctx.author.id == SUB_OWNER:
        channel = bot.get_channel(arg)
        if channel:
            await channel.purge()
            await channel.send("https://cdn.discordapp.com/attachments/428832869398347776/1151199255990640721/Grim_Dawn_Discord_Logo.png")
            await channel.send("https://cdn.discordapp.com/attachments/647753999948185611/647754106492026902/2a8e119d-e266-40d3-a9c8-a92194b658472Fdivider2.png")
            await channel.send(embed=welcome_embed)
            await channel.send("https://cdn.discordapp.com/attachments/647753999948185611/647754112661848094/2a8e119d-e266-40d3-a9c8-a92194b658472Fatt.png")
            await channel.send(embed=global_embed)
            await channel.send("https://cdn.discordapp.com/attachments/647753999948185611/647754128541614090/2a8e119d-e266-40d3-a9c8-a92194b658472Fchannel_rules.png")
            await channel.send(embed=channel_news_embed)
            await channel.send(embed=channel_gd_embed)
            await channel.send(embed=channel_community_embed)
            await channel.send(embed=channel_offtopic_embed)
            await channel.send("https://cdn.discordapp.com/attachments/647753999948185611/647754159034204160/2a8e119d-e266-40d3-a9c8-a92194b658472Fchat_roles.png")
            await channel.send(embed=chat_roles_embed)
            await channel.send("https://cdn.discordapp.com/attachments/647753999948185611/647754188469567488/2a8e119d-e266-40d3-a9c8-a92194b658472Fbuy_now.png")
            await channel.send(embed=buy_gd_embed)
            await channel.send(embed=buy_aom_embed)
            await channel.send(embed=buy_fg_embed)
            await channel.send(embed=buy_foa_embed)
            await channel.send("https://cdn.discordapp.com/attachments/647753999948185611/647754218198925312/2a8e119d-e266-40d3-a9c8-a92194b658472Flinkbase.png")
            await channel.send(embed=links_embed)
        else:
            await ctx.message.channel.send("Channel ID " + arg + " does not exist!")
    else:
        await ctx.message.channel.send("Nice try, kiddo!")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    elif message.content == "nerd":
        await message.channel.send("nerd")
        await message.delete()
    # elif "https://twitter.com" in message.content:
    #    await message.channel.send(message.content.replace("https://twitter.com", "https://vxtwitter.com"))
    #    await message.delete()
    elif "crab" in message.content:
        await message.add_reaction('🦀')

    await bot.process_commands(message)


@bot.command(aliases=['quit', 'q'])
async def shutdown(ctx):
    if ctx.author.id == OWNER_ID or ctx.author.id == SUB_OWNER:
        await ctx.message.delete()
        await ctx.bot.close()
    else:
        await ctx.message.channel.send("Nice try, kiddo!")


bot.run(TOKEN)
