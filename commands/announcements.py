import discord
from discord.ext import commands
import embeds

COMMAND_WHITELIST = {"Admin", "Moderator"}


class AnnouncementCommandCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.channel.send(f"Command on cooldown for **{round(error.retry_after, 1)}** seconds.")
        else:
            raise error

    @commands.has_permissions(manage_messages=True)
    @commands.command(aliases=['post-rules'])
    async def post_rules(self, ctx, arg):
        roles = {role.name for role in ctx.author.roles}
        if not COMMAND_WHITELIST.isdisjoint(roles):
            channel_id = int(arg)
            channel = self.bot.get_channel(channel_id)
            if channel:
                await channel.purge()
                await channel.send(
                    "https://cdn.discordapp.com/attachments/428832869398347776/1151199255990640721/Grim_Dawn_Discord_Logo.png")
                await channel.send(
                    "https://cdn.discordapp.com/attachments/647753999948185611/647754106492026902/2a8e119d-e266-40d3-a9c8-a92194b658472Fdivider2.png")
                await channel.send(embed=embeds.welcome_embed)
                await channel.send(
                    "https://cdn.discordapp.com/attachments/647753999948185611/647754112661848094/2a8e119d-e266-40d3-a9c8-a92194b658472Fatt.png")
                await channel.send(embed=embeds.global_embed)
                await channel.send(
                    "https://cdn.discordapp.com/attachments/647753999948185611/647754128541614090/2a8e119d-e266-40d3-a9c8-a92194b658472Fchannel_rules.png")
                await channel.send(embeds=[
                    embeds.channel_news_embed,
                    embeds.channel_gd_embed,
                    embeds.channel_community_embed,
                    embeds.channel_offtopic_embed
                ])
                await channel.send(
                    "https://cdn.discordapp.com/attachments/647753999948185611/647754159034204160/2a8e119d-e266-40d3-a9c8-a92194b658472Fchat_roles.png")
                await channel.send(embed=embeds.chat_roles_embed)
            else:
                await ctx.message.channel.send("Channel ID " + arg + " does not exist!")
        else:
            await ctx.message.channel.send("Nice try, kiddo!")

    @commands.has_permissions(manage_messages=True)
    @commands.command(aliases=['post-links'])
    async def post_links(self, ctx, arg):
        roles = {role.name for role in ctx.author.roles}
        if not COMMAND_WHITELIST.isdisjoint(roles):
            channel_id = int(arg)
            channel = self.bot.get_channel(channel_id)
            if channel:
                await channel.purge()
                await channel.send(
                    "https://cdn.discordapp.com/attachments/647753999948185611/647754188469567488/2a8e119d-e266-40d3-a9c8-a92194b658472Fbuy_now.png")
                await channel.send(embeds=[
                    embeds.buy_gd_embed,
                    embeds.buy_aom_embed,
                    embeds.buy_fg_embed,
                    embeds.buy_foa_embed
                ])
                await channel.send(
                    "https://cdn.discordapp.com/attachments/647753999948185611/647754218198925312/2a8e119d-e266-40d3-a9c8-a92194b658472Flinkbase.png")
                await channel.send(embed=embeds.links_embed)
            else:
                await ctx.message.channel.send("Channel ID " + arg + " does not exist!")
        else:
            await ctx.message.channel.send("Nice try, kiddo!")
