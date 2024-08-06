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
        name = channel.name
        pos = channel.position
        cat = channel.category
        new_ch = await channel.clone(name=name + "-t")
        await channel.delete()
        await new_ch.edit(name=name, position=pos, category=cat)
        logo = discord.File("images/Grim_Dawn_Discord_Logo.png")
        await new_ch.send(file=logo)
        divider = discord.File("images/divider.png")
        await new_ch.send(file=divider)
        # await channel.send(embed=embeds.welcome_embed)
        await new_ch.send(embeds.welcome_text)
        # attitude = discord.File("images/attitude.png")
        # await channel.send(file=attitude)
        await new_ch.send(embeds.global_text)
        await new_ch.send(embeds.global_text2)
        await new_ch.send(embeds.global_text3)
        # await channel.send(embed=embeds.global_embed)
        # await channel.send(embed=embeds.global_embed2)
        # await channel.send(embed=embeds.global_embed3)
        channel_rules = discord.File("images/channelRules.png")
        await new_ch.send(file=channel_rules)
        await new_ch.send(
            embeds=[
                embeds.channel_news_embed,
                embeds.channel_gd_embed,
                embeds.channel_community_embed,
                embeds.channel_offtopic_embed,
            ]
        )
        chat_roles = discord.File("images/chatRoles.png")
        await new_ch.send(file=chat_roles)
        await new_ch.send(embed=embeds.chat_roles_embed)
        await interaction.followup.send(
            f"Posted rules in {new_ch.mention}", ephemeral=True
        )

    @app_commands.command(name="post-links", description="Post the generated links")
    @app_commands.describe(channel="The channel in which to post the links")
    @app_commands.checks.has_any_role("Admin", "Moderator")
    async def post_links(
        self, interaction: discord.Interaction, channel: discord.TextChannel
    ):
        await interaction.response.defer(thinking=True, ephemeral=True)
        name = channel.name
        pos = channel.position
        cat = channel.category
        new_ch = await channel.clone(name=name + "-t")
        await channel.delete()
        await new_ch.edit(name=name, position=pos, category=cat)
        buy_now = discord.File("images/buynow.png")
        await new_ch.send(file=buy_now)
        await new_ch.send(
            embeds=[
                embeds.buy_gd_embed,
                embeds.buy_aom_embed,
                embeds.buy_fg_embed,
                embeds.buy_foa_embed,
            ]
        )
        links = discord.File("images/linkbase.png")
        await new_ch.send(file=links)
        await new_ch.send(embed=embeds.links_embed)
        await interaction.followup.send(
            f"Posted links in {new_ch.mention}", ephemeral=True
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
