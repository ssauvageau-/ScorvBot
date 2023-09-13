from contextlib import suppress
import discord
from discord.ext import commands

COMMAND_WHITELIST = {"Admin", "Moderator"}


class ModerationCommandCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def command_cooldown_generic(self, ctx):
        roles = {role.name for role in ctx.author.roles}
        if not COMMAND_WHITELIST.isdisjoint(roles):
            # whitelisted roles have no cooldown for this command structure
            return None
        elif "Janitor" in roles:
            # example exclusionary rule for Janitors
            return discord.app_commands.Cooldown(1, 15)
        else:
            return discord.app_commands.Cooldown(1, 30)

    @commands.command(aliases=['create-channel', 'cc'])
    @commands.dynamic_cooldown(command_cooldown_generic, type=commands.BucketType.user)
    async def create_channel(self, ctx, arg):
        roles = {role.name for role in ctx.author.roles}
        if not COMMAND_WHITELIST.isdisjoint(roles):
            guild = ctx.guild
            existing_channel = discord.utils.get(guild.channels, name=arg)
            if not existing_channel:
                await guild.create_text_channel(arg)
            await ctx.message.delete()

    @commands.command(aliases=['create-hidden-channel', 'chc', 'create-hidden'])
    @commands.dynamic_cooldown(command_cooldown_generic, type=commands.BucketType.user)
    async def create_hidden_channel(self, ctx, arg, *args):
        roles = {role.name for role in ctx.author.roles}
        if not COMMAND_WHITELIST.isdisjoint(roles):
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

    @commands.command(aliases=['create-hidden-channel-no-bot', 'chcnb'])
    @commands.dynamic_cooldown(command_cooldown_generic, type=commands.BucketType.user)
    async def create_hidden_channel_no_bot(self, ctx, arg, *args):
        roles = {role.name for role in ctx.author.roles}
        if not COMMAND_WHITELIST.isdisjoint(roles):
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

    @commands.command(aliases=['create-role', 'new-role', 'cr'])
    @commands.dynamic_cooldown(command_cooldown_generic, type=commands.BucketType.user)
    async def create_role(self, ctx, arg):
        roles = {role.name for role in ctx.author.roles}
        if not COMMAND_WHITELIST.isdisjoint(roles):
            guild = ctx.guild
            existing_role = discord.utils.get(guild.roles, name=arg)
            if not existing_role:
                await guild.create_role(name=arg)
                await ctx.message.delete()
            else:
                await ctx.message.channel.send("Role **" + arg + "** already exists!")

    @commands.command(aliases=['delete-role', 'dr'])
    @commands.dynamic_cooldown(command_cooldown_generic, type=commands.BucketType.user)
    async def delete_role(self, ctx, arg):
        roles = {role.name for role in ctx.author.roles}
        if not COMMAND_WHITELIST.isdisjoint(roles):
            guild = ctx.guild
            role = discord.utils.get(guild.roles, name=arg)
            if role:
                await role.delete()
                await ctx.message.delete()
            else:
                await ctx.message.channel.send("Role **" + arg + "** does not exist.")

    @commands.has_permissions(manage_messages=True)
    @commands.command(name='clear')
    @commands.dynamic_cooldown(command_cooldown_generic, type=commands.BucketType.user)
    async def clear(self, ctx, number: int = 1):
        await ctx.message.delete()
        roles = {role.name for role in ctx.author.roles}
        if not COMMAND_WHITELIST.isdisjoint(roles):
            with suppress(AttributeError):
                channel: discord.TextChannel = ctx.channel
                # TODO - Write waiting call for n > 5; this command otherwise makes too many requests above 5 deletions!
                if number > 5: number = 5
                async for m in channel.history(limit=number):
                    await m.delete()

    @commands.has_permissions(manage_messages=True)
    @commands.command(aliases=['clear-commands', 'clear-c'])
    @commands.dynamic_cooldown(command_cooldown_generic, type=commands.BucketType.user)
    async def clear_commands(self, ctx, number: int = 1):
        await ctx.message.delete()
        roles = {role.name for role in ctx.author.roles}
        if not COMMAND_WHITELIST.isdisjoint(roles):
            with suppress(AttributeError):
                channel: discord.TextChannel = ctx.channel
                # TODO - Write waiting call for n > 5; this command otherwise makes too many requests above 5 deletions!
                if number > 5: number = 5
                async for m in channel.history(limit=number):
                    if m.content[0] == "!":
                        await m.delete()


def setup(bot):
    bot.add_cog(ModerationCommandCog(bot))