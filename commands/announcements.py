import discord
from discord import app_commands
from discord.ext import commands
import embeds


@app_commands.guild_only()
class AnnouncementCommandGroup(app_commands.Group, name="announcements"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        super().__init__()

    @app_commands.command(name="post-rules", description="Post the generated rules")
    @app_commands.describe(channel="The channel in which to post the rules")
    @app_commands.checks.has_any_role("Admin", "Moderator")
    async def post_rules(
        self, interaction: discord.Interaction, channel: discord.TextChannel
    ):
        await interaction.response.defer(thinking=True, ephemeral=True)
        await channel.purge()
        logo = discord.File("images/Grim_Dawn_Discord_Logo.png")
        await channel.send(file=logo)
        divider = discord.File("images/divider.png")
        await channel.send(file=divider)
        await channel.send(embed=embeds.welcome_embed)
        attitude = discord.File("images/attitude.png")
        await channel.send(file=attitude)
        await channel.send(embed=embeds.global_embed)
        await channel.send(embed=embeds.global_embed2)
        channel_rules = discord.File("images/channelRules.png")
        await channel.send(file=channel_rules)
        await channel.send(
            embeds=[
                embeds.channel_news_embed,
                embeds.channel_gd_embed,
                embeds.channel_community_embed,
                embeds.channel_offtopic_embed,
            ]
        )
        chat_roles = discord.File("images/chatRoles.png")
        await channel.send(file=chat_roles)
        await channel.send(embed=embeds.chat_roles_embed)
        await interaction.followup.send(
            f"Posted rules in {channel.mention}", ephemeral=True
        )

    @app_commands.command(name="post-links", description="Post the generated links")
    @app_commands.describe(channel="The channel in which to post the links")
    @app_commands.checks.has_any_role("Admin", "Moderator")
    async def post_links(
        self, interaction: discord.Interaction, channel: discord.TextChannel
    ):
        await interaction.response.defer(thinking=True, ephemeral=True)
        await channel.purge()
        buy_now = discord.File("images/buynow.png")
        await channel.send(file=buy_now)
        await channel.send(
            embeds=[
                embeds.buy_gd_embed,
                embeds.buy_aom_embed,
                embeds.buy_fg_embed,
                embeds.buy_foa_embed,
            ]
        )
        links = discord.File("images/linkbase.png")
        await channel.send(file=links)
        await channel.send(embed=embeds.links_embed)
        await interaction.followup.send(
            f"Posted links in {channel.mention}", ephemeral=True
        )

    @post_rules.error
    @post_links.error
    async def missing_role_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ):
        if isinstance(error, app_commands.errors.MissingAnyRole):
            await interaction.response.send_message(
                "You do not have the required permissions to use this command!",
                ephemeral=True,
            )
        else:
            raise error
